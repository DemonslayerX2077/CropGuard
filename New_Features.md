# CropGuard — New Features Specification

## Overview

This document defines the two major features to be added to the existing CropGuard Android application:

1. **Hybrid Offline/Online Mode with Location and Server Synchronization**
2. **Offline-First Multilingual Text-Based Disease Suggestions and Step-by-Step Guidance**

The existing CropGuard prototype APK already performs on-device crop disease detection smoothly. These features must be integrated **without breaking or replacing the existing detection pipeline**.

### Core Design Principle

> **Internet must be an enhancement, never a dependency.**

The application must remain fully usable when the farmer has no internet connection. When connectivity becomes available, locally stored data should automatically synchronize with the backend.

---

# Feature 1: Hybrid Offline/Online Mode

## 1.1 Objective

CropGuard must support two operating conditions:

### Offline Mode
When internet connectivity is unavailable:

- On-device disease detection continues to work normally.
- User location should still be obtained when possible.
- Detection history is saved locally.
- Location coordinates are saved locally with the detection.
- Multilingual disease information remains available.
- No core feature should require an internet connection.

### Online Mode
When internet connectivity is available:

- All existing offline functionality continues to work.
- Detection history is stored locally first.
- Unsynchronized detection records are uploaded to the backend.
- User coordinates are synchronized with the corresponding detection record.
- Server-side storage can be used for analytics and future research.
- Synchronization should happen automatically without interrupting the user.

---

## 1.2 Recommended Architecture

Use an **offline-first architecture** rather than creating two separate applications.

```text
                    CropGuard App
                         |
                 ┌───────▼────────┐
                 │ Disease        │
                 │ Detection      │
                 │ On Device      │
                 └───────┬────────┘
                         |
                 ┌───────▼────────┐
                 │ Create         │
                 │ Detection      │
                 │ Record         │
                 └───────┬────────┘
                         |
                 ┌───────▼────────┐
                 │ Local Database │
                 │ Source of Truth│
                 └───────┬────────┘
                         |
              Internet Available?
                    /          \
                  NO            YES
                  |              |
            Keep locally    Sync to Server
                                 |
                         ┌───────▼────────┐
                         │ Backend / API  │
                         └────────────────┘
```

### Important Rule

**Always save the detection locally before attempting network synchronization.**

This prevents data loss if the network disappears immediately after detection.

---

# 1.3 Location System

## Recommended Approach

Do **not** manually triangulate three mobile towers inside the application.

Android's location services should be used to obtain the best available location. The application should use a fused location approach that can utilize:

- GPS/GNSS
- Cellular positioning
- Wi-Fi positioning
- Other available device location sources

### Important Clarification

GPS/GNSS does **not inherently require internet**.

Therefore:

- Offline mode can still attempt GPS/GNSS location.
- Network-based positioning can improve location availability when internet/network services are available.
- The app should use the best available location rather than artificially restricting GPS to online mode.

### Location Priority

Use the Android location APIs to request the best practical location for the device.

Store:

- Latitude
- Longitude
- Accuracy
- Timestamp
- Location availability/status

Example:

```text
Latitude: 16.xxxxx
Longitude: 74.xxxxx
Accuracy: 8.5 m
Timestamp: 2026-09-04T15:30:00
```

### Location Failure Handling

If a location cannot be obtained:

- Do NOT block disease detection.
- Save the detection without coordinates.
- Mark location as unavailable.
- Attempt to obtain location again where appropriate.
- Do not fabricate or estimate coordinates.

---

# 1.4 Detection History

Every detection should produce a structured local record.

Recommended fields:

```text
Detection ID
Disease ID
Disease Name
Confidence Score
Crop Name
Image Reference (if required)
Latitude
Longitude
Location Accuracy
Detection Timestamp
Language Used
Sync Status
```

### Sync Status

Use a simple state such as:

```text
PENDING
SYNCED
FAILED
```

Possible flow:

```text
Detection
   |
   ▼
Save Locally
   |
   ▼
PENDING
   |
Internet Available
   |
   ▼
Upload
   |
   ├── Success → SYNCED
   |
   └── Failure → FAILED/PENDING
```

---

# 1.5 Server Synchronization

When internet becomes available:

1. Detect network availability.
2. Query local database for unsynchronized records.
3. Upload pending records.
4. Confirm successful server response.
5. Mark records as `SYNCED`.
6. Retry failed uploads later.

### Requirements

- Synchronization must be automatic.
- Synchronization must not block the UI.
- Avoid duplicate server records.
- Use a unique detection ID for idempotent synchronization.
- Implement retry handling.
- Handle temporary network failures gracefully.

### Recommended Android Approach

Use Android background work facilities such as **WorkManager** for reliable synchronization.

Example concept:

```text
Network Available
       |
       ▼
WorkManager
       |
       ▼
Read Pending Records
       |
       ▼
Upload to API
       |
       ▼
Server Confirmation
       |
       ▼
Mark as Synced
```

---

# 1.6 Backend Expectations

The backend should provide an API for receiving detection records.

Example conceptual request:

```json
{
  "detectionId": "unique-id",
  "crop": "Tomato",
  "diseaseId": "TOMATO_EARLY_BLIGHT",
  "confidence": 0.94,
  "latitude": 16.000000,
  "longitude": 74.000000,
  "accuracy": 8.5,
  "timestamp": "2026-09-04T15:30:00Z"
}
```

The actual API structure should be adapted to the project's chosen backend.

### Backend Responsibilities

- Authenticate requests if authentication is implemented.
- Validate incoming data.
- Store detection records.
- Prevent duplicate records.
- Return clear success/failure responses.
- Support future analytics.

---

# Feature 2: Offline-First Multilingual Suggestions

## 2.1 Objective

CropGuard should provide disease information and actionable recommendations in the farmer's selected language.

The multilingual system must work **without internet**.

Initial recommended languages:

1. English
2. Marathi
3. Hindi

The architecture should make adding more Indian languages easy later.

---

# 2.2 Separate ML Detection from Language

The ML model should **not generate translated sentences**.

Instead, the ML model returns a stable disease identifier.

Example:

```text
ML Model
   |
   ▼
TOMATO_EARLY_BLIGHT
   |
   ▼
Localized Content
   |
   ▼
Selected Language
   |
   ▼
User-Friendly Result
```

This approach allows one ML model to support multiple languages.

---

# 2.3 Disease Content Structure

Each disease should have localized content containing:

- Disease name
- Short description
- Symptoms
- Recommended actions
- Step-by-step instructions
- Prevention tips
- Warning/precaution information

Example conceptual structure:

```text
Disease ID:
TOMATO_EARLY_BLIGHT

English:
  Name
  Description
  Symptoms
  Steps
  Prevention

Marathi:
  Name
  Description
  Symptoms
  Steps
  Prevention

Hindi:
  Name
  Description
  Symptoms
  Steps
  Prevention
```

---

# 2.4 Step-by-Step Recommendations

After detection, the application should clearly explain **what the farmer should do next**.

Example UI flow:

```text
Disease Detected
       |
       ▼
What is it?
       |
       ▼
Why did it happen?
       |
       ▼
What should you do?
       |
       ├── Step 1
       ├── Step 2
       ├── Step 3
       └── Step 4
       |
       ▼
Prevention Tips
```

Keep instructions:

- Simple
- Action-oriented
- Easy to understand
- Suitable for mobile screens
- Available offline

Avoid unnecessarily technical language.

---

# 2.5 Local Storage of Multilingual Content

Localized disease content should be packaged or stored locally so that it is available without internet.

Recommended implementation options:

### Option A — Android Resources

Use:

```text
res/values/strings.xml
res/values-mr/strings.xml
res/values-hi/strings.xml
```

Best for:

- Static UI text
- Buttons
- Navigation labels
- General application text

### Option B — Local JSON/Room Database

Use structured local content for:

- Disease descriptions
- Symptoms
- Step-by-step recommendations
- Prevention information

Recommended approach:

**Android Resources → UI translations**

**Local JSON/Room → Disease-specific multilingual content**

---

# 2.6 Online Multilingual Content Updates

When internet is available, the application may synchronize updated multilingual content from the server.

Online updates can provide:

- New disease information
- Improved recommendations
- Additional languages
- Updated translations
- Region-specific advice

However:

> The application must never depend on an online translation service for basic functionality.

If the server is unavailable, the application must immediately fall back to locally stored content.

---

# 2.7 Language Selection

Provide a simple language selector:

```text
Settings
   |
   ▼
Language
   |
   ├── English
   ├── मराठी
   └── हिन्दी
```

The selected language should be persisted locally.

On application restart, CropGuard should automatically use the previously selected language.

---

# 2.8 Fallback Logic

Use the following priority:

```text
Selected Language
       |
       ▼
Local Content Available?
      /       \
    YES        NO
    |           |
 Display      Fallback
 Content      Language
    |
    ▼
Internet Available?
    |
   YES
    |
Check for Updated Content
    |
    ▼
Update Local Cache
```

The application should always have a usable fallback.

---

# Combined CropGuard Architecture

The two features should work together.

```text
                         CropGuard
                            |
             ┌──────────────▼──────────────┐
             │      Camera / Image        │
             └──────────────┬──────────────┘
                            |
             ┌──────────────▼──────────────┐
             │   On-Device ML Detection   │
             └──────────────┬──────────────┘
                            |
                     Disease ID
                            |
              ┌─────────────▼─────────────┐
              │ Localized Disease Content │
              └─────────────┬─────────────┘
                            |
                 Selected Language
                            |
              ┌─────────────▼─────────────┐
              │ Explanation + Steps +     │
              │ Prevention Recommendations│
              └─────────────┬─────────────┘
                            |
                    Save Detection
                            |
              ┌─────────────▼─────────────┐
              │       Local Database      │
              │ Disease + Location + Time │
              │ + Confidence + Sync State │
              └─────────────┬─────────────┘
                            |
                    Network Available?
                       /           \
                     NO             YES
                     |               |
              Remain Offline     Background Sync
                                     |
                              ┌──────▼──────┐
                              │   Backend   │
                              └─────────────┘
```

---

# Technical Implementation Requirements

## Preserve Existing Functionality

The existing APK already performs disease detection successfully.

The agent must:

- Inspect the current project before modifying it.
- Understand the existing architecture.
- Reuse existing ML inference code.
- Avoid unnecessary rewrites.
- Avoid replacing a working detection pipeline.
- Keep the current UI functional unless changes are required.
- Add the new features modularly.

---

# Suggested Android Components

Adapt these to the existing project rather than introducing unnecessary dependencies.

### Local Storage

Prefer:

- Room Database for structured detection history.
- DataStore for lightweight settings such as selected language.

### Location

Use Android's modern location APIs / fused location provider.

### Network Detection

Use Android connectivity APIs to determine whether a usable network is available.

### Background Synchronization

Use WorkManager for:

- Pending detection synchronization
- Retrying failed uploads
- Optional content updates

### Networking

Use the project's existing networking stack if one already exists.

If no networking layer exists, use a clean API abstraction such as Retrofit/OkHttp where appropriate.

---

# Data Models

## DetectionRecord

Conceptual model:

```kotlin
DetectionRecord(
    id: String,
    crop: String,
    diseaseId: String,
    diseaseName: String,
    confidence: Float,
    latitude: Double?,
    longitude: Double?,
    accuracy: Float?,
    timestamp: Long,
    language: String,
    syncStatus: SyncStatus
)
```

The actual implementation should follow the project's existing architecture and naming conventions.

---

# Privacy and Permission Requirements

Location is sensitive data and must be handled carefully.

The app should:

- Request location permission only when needed.
- Explain why location is required.
- Continue disease detection if the user denies location permission.
- Never fabricate coordinates.
- Send coordinates to the server only according to the application's documented behavior and user permissions.
- Store only the minimum location information required by the project.
- Avoid collecting unnecessary personal information.

The UI should clearly communicate that location is used to associate disease detections with geographic areas.

---

# UX Requirements

The farmer should not need to understand whether the application is currently online or offline.

Recommended small status indicator:

```text
● Offline
```

or

```text
● Online — Syncing
```

or

```text
✓ Synced
```

The status should be informative but should not interfere with the main detection workflow.

### Example User Experience

```text
1. Farmer opens CropGuard.
2. Selects preferred language.
3. Takes a crop image.
4. ML model detects the disease offline.
5. CropGuard displays disease name and confidence.
6. CropGuard shows explanation and step-by-step recommendations.
7. App attempts to obtain location.
8. Detection + available location are saved locally.
9. If internet is available, the record is synchronized.
10. If internet is unavailable, the record remains safely stored.
11. When internet returns, pending records synchronize automatically.
```

---

# Error Handling

The application must gracefully handle:

### No Internet

```text
Continue normally.
Store data locally.
```

### No GPS/Location

```text
Continue detection.
Save record without location.
```

### Permission Denied

```text
Continue detection.
Explain optional location functionality.
```

### Server Failure

```text
Keep record locally.
Mark as pending/failed.
Retry later.
```

### Translation Missing

```text
Use the configured fallback language.
Never show a blank recommendation.
```

---

# Testing Checklist

## Offline Testing

- [ ] Disable Wi-Fi and mobile data.
- [ ] Perform disease detection.
- [ ] Verify detection works.
- [ ] Verify multilingual content works.
- [ ] Verify step-by-step recommendations work.
- [ ] Verify location can be obtained when available.
- [ ] Verify detection is saved locally.
- [ ] Verify the app does not crash without internet.

## Online Testing

- [ ] Enable internet.
- [ ] Perform a new detection.
- [ ] Verify local record is created.
- [ ] Verify server synchronization occurs.
- [ ] Verify coordinates are uploaded when available.
- [ ] Verify sync status changes to `SYNCED`.

## Network Interruption Testing

- [ ] Start detection with internet.
- [ ] Disable internet during/after detection.
- [ ] Verify data is not lost.
- [ ] Re-enable internet.
- [ ] Verify pending data synchronizes.

## Multilingual Testing

- [ ] English UI/content.
- [ ] Marathi UI/content.
- [ ] Hindi UI/content.
- [ ] Language persists after restart.
- [ ] Disease recommendations are translated.
- [ ] No missing strings.
- [ ] Fallback language works.

## Location Testing

- [ ] GPS available.
- [ ] GPS unavailable.
- [ ] Location permission granted.
- [ ] Location permission denied.
- [ ] Low-accuracy location.
- [ ] Location temporarily unavailable.

---

# Development Priorities

Implement the features in this order:

## Phase 1 — Project Analysis

- Inspect the existing CropGuard codebase.
- Identify current ML inference flow.
- Identify current history/storage implementation.
- Identify current UI architecture.
- Identify current dependencies.

## Phase 2 — Local Data Layer

- Add/upgrade local detection history.
- Add location fields.
- Add sync status.
- Ensure all detections are saved locally.

## Phase 3 — Location

- Integrate Android location services.
- Request permissions correctly.
- Store latitude, longitude, accuracy, and timestamp.
- Ensure detection remains functional without location.

## Phase 4 — Hybrid Synchronization

- Add network availability detection.
- Implement backend API integration.
- Add WorkManager synchronization.
- Implement retries and duplicate protection.

## Phase 5 — Multilingual System

- Add language selection.
- Add English, Marathi, and Hindi.
- Localize UI.
- Create local disease-content structure.
- Add disease explanations and step-by-step recommendations.

## Phase 6 — Online Content Sync

- Add optional server-side content updates.
- Cache updated content locally.
- Ensure offline fallback always works.

## Phase 7 — Testing and Polish

- Test offline-first behavior.
- Test synchronization.
- Test location edge cases.
- Test all supported languages.
- Improve UI feedback.
- Verify no existing functionality has regressed.

---

# Definition of Done

The implementation is considered complete when:

- [ ] CropGuard disease detection works completely offline.
- [ ] Detection history is stored locally.
- [ ] Location can be obtained without requiring internet.
- [ ] Location is attached to detection records when available.
- [ ] Online connectivity triggers background synchronization.
- [ ] Server receives detection history and coordinates.
- [ ] Failed synchronization does not cause data loss.
- [ ] English, Marathi, and Hindi are supported.
- [ ] Disease explanations are available offline.
- [ ] Step-by-step recommendations are available offline.
- [ ] Language preference persists.
- [ ] Online content can enhance/update local content without becoming a dependency.
- [ ] Existing ML detection functionality remains intact.
- [ ] The app gracefully handles missing internet, location, permissions, and server failures.
- [ ] The complete workflow has been tested on a real Android device.

---

# Agent Instructions

You are modifying an **existing working CropGuard Android application**, not creating a new application from scratch.

Before writing code:

1. Inspect the entire existing project structure.
2. Identify the current architecture and technology stack.
3. Locate the ML model/inference pipeline.
4. Locate existing history/storage functionality.
5. Reuse existing components wherever practical.
6. Identify the minimum changes required for these features.

Then implement the features incrementally.

### Critical Constraints

- Do not move disease inference to the cloud.
- Do not make internet mandatory for detection.
- Do not manually triangulate mobile towers.
- Do not fabricate location data.
- Do not require internet for multilingual disease guidance.
- Do not replace the working ML model unless technically necessary.
- Do not delete existing functionality.
- Do not introduce unnecessary dependencies.
- Handle permissions and privacy responsibly.
- Keep the architecture maintainable and scalable.

### Final Goal

Transform the current CropGuard prototype into a robust:

> **Offline-first, multilingual, location-aware crop disease detection application with automatic online synchronization.**

The farmer should be able to use the application in a field with **zero internet connectivity**, while the system should automatically take advantage of connectivity whenever it becomes available.
