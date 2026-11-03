# CropGuard 🌱
### Offline-First Android Crop Disease Detection & Agricultural Advisory System

<p align="center">
  <strong>On-device AI • Offline-first design • Multilingual guidance • Optional data synchronization</strong>
</p>

CropGuard is an Android application project focused on helping users identify selected crop-leaf diseases using machine learning directly on a mobile device. Its design prioritizes rural and resource-constrained environments where internet access may be unreliable.

The project combines an edge-inference approach with a local disease-information repository. Its proposed extended architecture also supports geotagged scan history and optional background synchronization when connectivity is available.

> **Important — implementation status:** The supplied project documents describe both a mock-only UI development stage and a more complete TFLite/Room/WorkManager architecture. This README therefore documents the intended system and the capabilities recorded in the project materials; it does not imply that every component is present in every repository revision. Check the source code and test results in the current branch before treating any feature or benchmark as verified.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Key Design Principles](#key-design-principles)
- [Features](#features)
- [Machine Learning Model](#machine-learning-model)
- [Supported Crops and Classes](#supported-crops-and-classes)
- [Input Validation and OOD Detection](#input-validation-and-ood-detection)
- [Offline-First Architecture](#offline-first-architecture)
- [Multilingual Disease Guidance](#multilingual-disease-guidance)
- [Detection History, Location and Synchronization](#detection-history-location-and-synchronization)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Optional Mock Backend](#running-the-optional-mock-backend)
- [Testing](#testing)
- [Reported Model Evaluation](#reported-model-evaluation)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Privacy and Responsible Use](#privacy-and-responsible-use)
- [Research References](#research-references)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

CropGuard explores how lightweight computer vision models can be deployed on Android devices to make crop-leaf disease classification available without requiring a cloud inference service.

The documented model pipeline uses **MobileNetV3-Small**, converted to **TensorFlow Lite** and described as Float16-quantized. The model is intended to classify leaf images into 38 classes across 14 crop categories. Disease identifiers are resolved against locally stored disease information so that explanations and recommendations can be displayed without calling an online translation service.

The broader system design includes:

- Android-based image capture and selection.
- On-device image classification.
- Input screening and uncertainty handling.
- Locally stored disease information in English, Hindi and Marathi.
- Local scan history.
- Optional location metadata.
- Optional background synchronization to a configurable backend.

### Project Goals

1. Make crop-leaf disease classification usable in low-connectivity environments.
2. Keep the core inference path on the Android device.
3. Provide understandable disease information in multiple Indian languages.
4. Preserve scan records locally before attempting any network operation.
5. Make the application modular enough to support future research and feature extensions.

---

## Problem Statement

Farmers may have limited access to timely plant-health advice, particularly when specialist support or reliable connectivity is unavailable. Cloud-dependent image recognition can introduce network latency, data costs and service-availability problems.

CropGuard investigates an alternative: run the image-classification model on the phone, retrieve disease guidance from local assets, and treat internet connectivity as an optional enhancement rather than a requirement for core detection.

---

## Key Design Principles

| Principle | Meaning |
|---|---|
| **Offline first** | Core detection and locally packaged disease guidance should not depend on internet access. |
| **On-device inference** | Crop images are processed by the mobile application rather than requiring cloud-based model inference. |
| **Local-first persistence** | Save a detection locally before attempting synchronization. |
| **Language-independent model output** | The model returns a class label/identifier; the local knowledge base supplies the selected language. |
| **Graceful degradation** | Missing location, internet or server availability should not prevent a scan from being completed. |
| **Incremental development** | Extend the existing Android project without unnecessarily replacing a working detection pipeline. |

---

## Features

The following list combines features described in the project documentation. Their implementation should be checked against the current source branch.

### Core application and AI

- Android application built with Kotlin.
- MobileNetV3-Small image-classification model.
- TensorFlow Lite model deployment for on-device inference.
- 224 × 224 RGB model input as documented.
- 38 output classes across 14 crop categories.
- Confidence score and disease information display.
- Input screening and uncertainty-rejection logic.

### Disease information

- Local disease knowledge base.
- English, Hindi and Marathi content datasets.
- Disease descriptions and symptom information.
- Treatment and prevention guidance.
- Language selection stored as an application preference.

### Offline-first data handling

- Local detection history using Room/SQLite in the documented architecture.
- Detection metadata such as crop, disease, confidence and timestamp.
- Optional image reference and location metadata.
- Pending/synced/failed synchronization states.

### Optional online capabilities

- Configurable backend URL.
- Background synchronization using WorkManager.
- Retry handling for temporary network/server failures.
- A lightweight Python mock server and browser dashboard are documented for local synchronization testing.

---

## Machine Learning Model

### Model architecture

| Property | Documented value |
|---|---|
| Architecture | MobileNetV3-Small |
| Runtime | TensorFlow Lite |
| Quantization | Float16 |
| Input shape | 224 × 224 × 3 (RGB) |
| Output classes | 38 |
| Crop categories | 14 |
| Documented model size | Approximately 4.57 MB |
| Dataset named in project report | PlantVillage |

MobileNetV3-Small is intended for mobile and edge environments where model size, memory use and inference time matter.

### Model pipeline

```text
Leaf image
    │
    ▼
Image preprocessing
    │
    ▼
Input screening
    │
    ▼
TensorFlow Lite / MobileNetV3-Small
    │
    ▼
38-class prediction scores
    │
    ▼
Confidence and uncertainty checks
    │
    ▼
Disease class identifier
    │
    ▼
Localized disease information
    │
    ▼
Result and recommendations
```

### Quantization

The project documentation describes converting a floating-point model to a Float16 TensorFlow Lite model. It reports a reduction from approximately 10.2 MB to 4.57 MB.

Quantization can reduce model storage and deployment overhead. Actual latency, memory use and accuracy depend on the target device and runtime; they should be measured on the devices used for evaluation.

---

## Supported Crops and Classes

The documented class list contains the following 14 crop categories and 38 labels:

| Crop | Documented classes |
|---|---|
| Apple | Apple Scab, Black Rot, Cedar Apple Rust, Healthy |
| Blueberry | Healthy |
| Cherry | Powdery Mildew, Healthy |
| Corn (Maize) | Cercospora Leaf Spot / Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| Grape | Black Rot, Esca (Black Measles), Leaf Blight, Healthy |
| Orange (Citrus) | Huanglongbing (Citrus Greening) |
| Peach | Bacterial Spot, Healthy |
| Pepper (Bell) | Bacterial Spot, Healthy |
| Potato | Early Blight, Late Blight, Healthy |
| Raspberry | Healthy |
| Soybean | Healthy |
| Squash | Powdery Mildew |
| Strawberry | Leaf Scorch, Healthy |
| Tomato | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Two-Spotted Spider Mite Damage, Target Spot, Tomato Yellow Leaf Curl Virus, Tomato Mosaic Virus, Healthy |

**Scope note:** These are the classes listed in the supplied project documentation. They do not mean that the application can diagnose every crop, every disease, or every field condition. A crop/disease combination not represented in the model's labels is outside the documented classifier scope.

---

## Input Validation and OOD Detection

A standard closed-set classifier always distributes its output across the classes it knows. As a result, an unrelated image may still receive a seemingly confident class prediction.

The documented CropGuard design describes two screening stages:

1. **Vegetation/colorimetric screening:** Samples image pixels in HSV color space and estimates whether enough pixels fall within selected vegetation/disease-color ranges.
2. **Prediction uncertainty screening:** Uses the model's output confidence and normalized Shannon entropy to flag uncertain inputs.

The documented example thresholds are:

- Vegetation pixel ratio threshold: 5%.
- Minimum top prediction confidence: 0.50.
- Normalized entropy rejection threshold: 0.82.

These are implementation parameters, not proof that all non-leaf images or unfamiliar field images will be rejected correctly. Color-based screening can be affected by lighting, backgrounds, leaf color and disease symptoms. OOD performance must be evaluated using representative in-distribution and out-of-distribution test images.

---

## Offline-First Architecture

The central architecture rule is:

> **Internet must be an enhancement, never a dependency.**

```text
             Android application
                     │
                     ▼
              Capture/select image
                     │
                     ▼
             On-device classifier
                     │
                     ▼
             Disease class identifier
                     │
                     ▼
          Local multilingual knowledge base
                     │
                     ▼
            Display diagnosis/advice
                     │
                     ▼
             Save detection locally
                     │
                     ▼
             Network available?
                 /        \
               No          Yes
               │            │
        Keep record      Queue background
         on device          synchronization
                               │
                               ▼
                         Configured API
```

The local database is intended to remain the source of truth for scan history. A network failure should not discard a detection or interrupt the user-facing diagnosis flow.

---

## Multilingual Disease Guidance

The documented language set is:

- English
- Hindi (हिन्दी)
- Marathi (मराठी)

The model should return a stable class identifier rather than generating translated text. The application then looks up that identifier in the corresponding local language data file.

Documented asset names:

```text
disease_info_en.json
disease_info_hi.json
disease_info_mr.json
```

The disease-information schema may include:

- Crop name
- Disease name
- Description
- Symptoms
- Treatment
- Step-by-step actions
- Prevention guidance

Static interface translations and disease-specific advisory content are separate concerns. The project history notes that translating the disease knowledge base does not automatically translate hardcoded UI labels; all visible interface strings should use Android's resource-based localization.

---

## Detection History, Location and Synchronization

### Local detection record

The documented data model includes fields such as:

- Unique detection ID
- Crop and disease identifiers
- Disease name
- Confidence score
- Timestamp
- Selected language
- Optional image reference
- Optional latitude and longitude
- Optional location accuracy
- Synchronization status

### Location behavior

The proposed Android implementation uses the Fused Location Provider and may use GPS/GNSS, cellular and Wi-Fi signals where available.

Location is optional. If permission is denied or a location fix is unavailable, the application should still complete the scan and save the record without coordinates. The application must never fabricate location data.

### Background synchronization

The documented synchronization flow uses:

- Room/SQLite for local persistence.
- Android connectivity monitoring.
- WorkManager for deferrable background work.
- A REST endpoint for batch upload.

The development history records a mock endpoint:

```http
POST /api/v1/detections/sync
GET  /api/v1/detections
POST /api/v1/detections/clear
```

The history also describes a Python standard-library mock server that stores received records in `server/detections_db.json` and serves a local dashboard. This is a development/testing backend, not a production hosting or security design.

---

## Technology Stack

The supplied documentation lists the following technologies. Confirm exact versions in the repository's Gradle files before building.

| Area | Technology |
|---|---|
| Platform | Android |
| Primary language | Kotlin |
| UI | Jetpack Compose, Material 3 |
| ML model | MobileNetV3-Small |
| ML runtime | TensorFlow Lite |
| Camera | CameraX |
| Local database | Room / SQLite |
| Background work | WorkManager |
| Location | Google Play Services Fused Location Provider |
| Networking | Retrofit / OkHttp |
| Serialization | Gson |
| Image loading | Coil |
| Optional mock backend | Python 3 standard library |

---

## Project Structure

The following is a **logical reference structure** based on the project documentation. Your actual repository may differ; do not move existing files solely to match this example.

```text
CropGuard/
├── android/
│   └── app/
│       └── src/main/
│           ├── assets/
│           │   ├── model.tflite
│           │   ├── labels.txt
│           │   ├── disease_info_en.json
│           │   ├── disease_info_hi.json
│           │   └── disease_info_mr.json
│           ├── java/com/cropdisease/app/
│           │   ├── MainActivity.kt
│           │   ├── DiseaseRepository.kt
│           │   ├── data/
│           │   │   ├── Classifier.kt
│           │   │   ├── Prediction.kt
│           │   │   ├── ScanResult.kt
│           │   │   └── local/
│           │   ├── location/
│           │   ├── navigation/
│           │   ├── network/
│           │   ├── sync/
│           │   └── ui/
│           │       ├── components/
│           │       ├── screens/
│           │       └── theme/
│           └── res/
├── ml/
│   ├── train.py
│   ├── convert_to_tflite.py
│   └── evaluate_tflite.py
├── server/
│   └── server.py
├── docs/
├── README.md
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Android Studio with a compatible Android SDK.
- JDK version compatible with the project's Gradle configuration (the supplied documentation mentions JVM 17).
- Android device or emulator.
- Git.
- Python 3 only if you intend to run the optional mock backend.

### Clone the repository

```bash
git clone https://github.com/DemonslayerX2077/CropGuard/
cd CropGuard
```

### Open the Android project

1. Open Android Studio.
2. Select **Open** and choose the Android project directory (the folder containing the relevant Gradle settings file).
3. Allow Gradle sync to complete.
4. Connect an Android device with USB debugging enabled, or start an emulator.
5. Build and run the application using Android Studio.

> The exact project root and build variant depend on the repository layout. Follow the Gradle files committed to the current branch.

### Install a generated APK

If a debug APK has been built, it is commonly located at:

```text
android/app/build/outputs/apk/debug/app-debug.apk
```

Install it with ADB:

```bash
adb install -r android/app/build/outputs/apk/debug/app-debug.apk
```

The APK path above is the path documented by the project; it will exist only after a successful build.

---

## Running the Optional Mock Backend

The development history documents a lightweight Python mock server for testing synchronization.

From the repository root:

```bash
cd server
python server.py
```

Then open:

```text
http://localhost:8000/
```

For an Android emulator, the documented default base URL is:

```text
http://10.0.2.2:8000/
```

For a physical Android device, configure the server URL to use the computer's reachable local-network IP address. The phone and computer generally need to be on the same network, and the computer firewall must permit the connection.

The mock backend is intended for local development. Do not expose it publicly or use it to store real farmer/location data without adding appropriate authentication, transport security, validation, access control and privacy safeguards.

---

## Testing

Use the following checklist when validating a build.

### Model and image pipeline

- [ ] Confirm the TFLite model and label file are packaged in the APK.
- [ ] Verify the expected input dimensions and preprocessing.
- [ ] Test representative images for every supported class.
- [ ] Record per-class precision, recall and F1-score.
- [ ] Test low-confidence predictions.
- [ ] Test unrelated images and difficult backgrounds for OOD behavior.
- [ ] Measure inference latency on real Android devices.

### Offline behavior

- [ ] Disable Wi-Fi and mobile data.
- [ ] Confirm that the app opens and core detection remains available.
- [ ] Confirm disease descriptions and selected-language content load locally.
- [ ] Confirm scans are retained locally.
- [ ] Confirm the app handles missing location permission and unavailable GPS.

### Synchronization

- [ ] Enable connectivity and configure the mock backend URL.
- [ ] Create a detection and confirm that a local record is saved first.
- [ ] Trigger synchronization.
- [ ] Confirm the backend receives the expected record.
- [ ] Interrupt the network and verify that pending records are retained.
- [ ] Restore connectivity and verify retry behavior.
- [ ] Check that repeated sync attempts do not create duplicate records.

### Localization

- [ ] Check English, Hindi and Marathi disease information.
- [ ] Check static UI labels in each language.
- [ ] Restart the app and confirm the selected language persists.
- [ ] Confirm a fallback is shown if a translation entry is missing.

---

## Reported Model Evaluation

The supplied project README reports the following evaluation results for a 5,430-image test split:

| Metric | Reported result |
|---|---:|
| Top-1 accuracy | 98.84% |
| Top-3 accuracy | 99.72% |
| Macro precision | 98.61% |
| Macro recall | 98.54% |
| Macro F1-score | 98.57% |
| Validation loss | 0.0521 |

It also reports mobile inference measurements ranging from 24 ms to 112 ms across the listed devices.

> **Reproducibility note:** These are figures stated in the supplied project documentation, not independently verified by this README. Before using them in a paper, poster or public release, retain the evaluation scripts, dataset split details, model version, device details and raw results. PlantVillage-style curated test performance should not be presented as proof of equivalent accuracy on real-world field images.

---

## Limitations

The project documentation identifies or implies the following limitations:

1. **Dataset coverage:** The documented classifier is limited to the 38 labels listed above.
2. **Field domain gap:** Curated leaf datasets may not represent varied field lighting, camera quality, backgrounds, leaf age and regional crop varieties.
3. **Multiple diseases:** A single-label classifier may not represent multiple simultaneous infections on one leaf.
4. **Visible symptoms only:** Leaf-image classification cannot reliably identify conditions that require root, stem, fruit or laboratory examination.
5. **OOD screening:** Color and confidence/entropy thresholds can reject some invalid inputs but cannot guarantee that every unfamiliar image will be detected.
6. **Agricultural recommendations:** Treatment advice should be reviewed by qualified agricultural experts and adapted to local regulations, crop stage and conditions.
7. **Location availability:** GPS accuracy and availability vary by device, environment and permission state.
8. **Implementation status:** The project documents describe different development stages. Current source code and device testing determine which components are actually available in a given release.

CropGuard should be treated as an informational decision-support tool, not a replacement for a qualified agronomist or plant pathologist.

---

## Roadmap

The supplied feature specification proposes the following development priorities:

- [ ] Verify and document the current Android architecture and inference pipeline.
- [ ] Complete or validate persistent local detection history.
- [ ] Add optional location metadata with permission-aware fallback.
- [ ] Complete reliable background synchronization and duplicate protection.
- [ ] Ensure full UI localization in English, Hindi and Marathi.
- [ ] Expand structured, offline disease explanations and step-by-step guidance.
- [ ] Add optional online content updates while retaining local fallback.
- [ ] Evaluate model robustness on real-world field images.
- [ ] Improve OOD detection using a representative validation dataset.
- [ ] Conduct device-level performance, battery and usability testing.
- [ ] Explore severity estimation, offline text-to-speech and privacy-preserving model improvement as future research directions.

---

## Privacy and Responsible Use

- Crop images should be processed on-device for inference as described by the project architecture.
- Location access should be optional, requested only when needed and explained to the user.
- A scan should not fail solely because location permission is denied.
- Detection records should be stored locally before any upload is attempted.
- Synchronization should send only the fields required by the configured backend.
- Do not commit API keys, signing keys, passwords, private credentials or real user/farmer records.
- Review model and dataset licenses before redistributing model weights or datasets.
- Do not publish location-bearing test records or private images in the repository.

---

## Research References

The project documentation lists these foundational references:

1. Howard, A. et al. (2019). *Searching for MobileNetV3*. Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 1314–1324.
2. Hughes, D. P., & Salathé, M. (2015). *An open access repository of images on plant health to enable the development of mobile disease diagnostics*. arXiv:1511.08060.
3. Sandler, M. et al. (2018). *MobileNetV2: Inverted Residuals and Linear Bottlenecks*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 4510–4520.
4. Mohanty, S. P., Hughes, D. P., & Salathé, M. (2016). *Using deep learning for image-based plant disease detection*. Frontiers in Plant Science, 7, 1419.
5. Google Developers. *TensorFlow Lite for mobile and edge devices*.
6. Android Developers. *Guide to app architecture* and Jetpack Compose documentation.

---

## Contributing

Contributions, bug reports and research improvements are welcome.

When proposing a change:

1. Describe the problem or research motivation.
2. Include reproduction steps for bugs.
3. Keep the offline-first behavior intact.
4. Avoid replacing working model or storage components without evidence.
5. Include tests or evaluation results where applicable.
6. Document whether a feature is implemented, experimental or planned.

---

## License

No license has been confirmed in the supplied project files. Until a license is added to the repository, assume that the source is **not licensed for reuse or redistribution**.

Before publishing, choose a license that matches the project's ownership, institutional requirements and third-party model/dataset licenses, then add the corresponding `LICENSE` file.

---

<p align="center">
  <strong>CropGuard — Practical Edge AI for More Accessible Crop Health Support 🌱</strong>
</p>

