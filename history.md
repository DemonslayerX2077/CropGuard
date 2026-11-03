# CropGuard — Conversation & Development History Log

**Project:** Crop Disease Detection (CropGuard Android App & Mock Sync Backend)  
**Date:** September 5, 2026  

---

## 1. Summary of Topics & Questions Discussed

### Q1: Multilanguage (Hindi, Marathi, English) Behavior
* **Question**: Why does nothing change across the app when switching the language to Hindi or Marathi?
* **Analysis**:
  - The static UI screens ([HomeScreen.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/ui/screens/HomeScreen.kt), [SettingsScreen.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/ui/screens/SettingsScreen.kt), [HistoryScreen.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/ui/screens/HistoryScreen.kt)) used hardcoded English string literals instead of dynamic Android resource resolution (`stringResource`).
  - The language preference was only wired to the **AI Knowledge Base** (`DiseaseRepository.kt`), meaning changing the language dynamically translates the **Crop Name, Disease Name, Description, Prevention Steps, and Treatments** from `disease_info_hi.json` / `disease_info_mr.json` for subsequent leaf scans, but left the surrounding menu headers in English.

---

### Q2: Automatic Server Synchronization Architecture
* **Question**: How does Automatic Server Synchronization save and manage data?
* **Analysis & Architecture**:
  - **Offline-First Storage**: Detections are immediately persisted locally in SQLite via Room DB (`DetectionEntity`) with `syncStatus = 0` (`PENDING`).
  - **WorkManager**: Background worker `DetectionSyncWorker` queries unsynced records and sends them in batch to `POST /api/v1/detections/sync`.
  - **Success Handling**: When the server returns `200 OK`, `syncStatus` is updated to `1` (`SYNCED`).
  - **Fault Tolerance**: If offline or if the server is unreachable, records remain safe on the device with automatic exponential backoff retry.

---

### Q3: In-App Local Database Access
* **Question**: How can a user access and view the local database data through the app itself?
* **Solution**:
  - **Recent Scans** on the Home Screen displays real-time items from Room DB.
  - **Scan History Screen ([HistoryScreen.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/ui/screens/HistoryScreen.kt))** displays all historical diagnoses with thumbnail photos, GPS coordinates, confidence bars, and **live sync status badges** (🟢 Synced, ⚪ Pending, 🔴 Failed).
  - **Detail View ([DiseaseDetailScreen.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/ui/screens/DiseaseDetailScreen.kt))** displays complete symptoms, treatments, and prevention advice.

---

### Q4: Sync Timing & Fast Sync
* **Discussion**: Can the 2-hour periodic sync timer be decreased to 5 seconds?
* **Resolution**:
  - Clarified that Android OS WorkManager enforces a minimum 15-minute interval for `PeriodicWorkRequest` to preserve battery.
  - Clarified that immediate sync is already triggered automatically upon leaf scan completion.
  - The user explicitly requested **not** to add the 5-second polling loop to keep the app clean and battery-efficient.

---

## 2. Implemented Features & Changes

### A. Zero-Dependency Mock Server & Live Dashboard
* Created [server/server.py](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/server/server.py):
  * Runs on Python 3 standard library (`http.server`) with zero external pip dependencies.
  * Implements `POST /api/v1/detections/sync` (batch upload), `GET /api/v1/detections` (JSON), and `POST /api/v1/detections/clear`.
  * Hosts a sleek real-time web dashboard at `http://localhost:8000/` with auto-refreshing stats and detection tables.
  * Persists records to `server/detections_db.json`.

### B. Android App Updates
1. **[AndroidManifest.xml](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/AndroidManifest.xml)**:
   * Added `android:usesCleartextTraffic="true"` to allow local HTTP testing.
2. **[PreferencesManager.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/data/PreferencesManager.kt)**:
   * Added `serverUrl` preference with default `http://10.0.2.2:8000/`.
3. **[CropGuardApi.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/network/CropGuardApi.kt)**:
   * Dynamic base URL resolution from `PreferencesManager`.
4. **[DetectionSyncWorker.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/sync/DetectionSyncWorker.kt)**:
   * Updated to use dynamic `ApiClient.getService(applicationContext)`.
5. **[SettingsScreen.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/ui/screens/SettingsScreen.kt)**:
   * Added **"Server Sync & Network"** section with editable Server URL and **"Sync Now with Server"** button.
6. **[HistoryScreen.kt](file:///c:/Users/Aditya/Desktop/CropDiseaseDetection/android/app/src/main/java/com/cropdisease/app/ui/screens/HistoryScreen.kt)**:
   * Added top app bar sync action icon.

---

## 3. How to Run and Test

1. **Start Mock Server**:
   ```bash
   cd c:\Users\Aditya\Desktop\CropDiseaseDetection\server
   python server.py
   ```
2. **Open Dashboard**:
   Open [http://localhost:8000/](http://localhost:8000/) in your browser.
3. **Rebuild Android App**:
   In Android Studio, click **Run (▶)** to install the updated APK.
4. **Test Synchronization**:
   * Open **Settings > Server Sync & Network**.
   * Confirm URL (`http://10.0.2.2:8000/` for Emulator or your PC's IP for physical devices).
   * Tap **"Sync Now with Server"** or scan a leaf.
   * View the incoming sync record live on the browser dashboard.
