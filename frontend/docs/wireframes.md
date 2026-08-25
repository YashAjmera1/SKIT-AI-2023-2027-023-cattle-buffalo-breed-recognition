# UI/UX Design & Wireframe Specifications
**Project:** Image-Based Breed Recognition System for Cattle & Buffalo in India  
**Project ID:** SKIT/AI/2023-2027/023  
**Designer:** Yash Ajmera (CSE-AI, Roll: 23ESKCA125)  
**Date:** August 2026

---

## 1. Design Overview & Objectives
The goal of this UI/UX design is to deliver an intuitive, clean, and highly responsive single-page application (SPA) tailored for Indian dairy farmers, veterinary researchers, and livestock enumerators. The application allows users to upload an image of an indigenous cattle or buffalo and instantly receive breed identification alongside rich breed metadata.

### Core UX Principles:
- **Clarity over Complexity:** High visual hierarchy with minimal cognitive load.
- **Immediate Feedback:** Clear visual states for idle, file dragging, validating, analyzing, success, and error.
- **Contextual Breed Intelligence:** Beyond simply predicting a label, the system displays origin, daily milk yield, and primary use (Dairy / Draught / Dual-purpose).
- **Accessibility:** High-contrast text, clear iconography, WCAG AA compliance, and mobile-friendly touch targets.

---

## 2. Color Palette & Typography

### Primary Palette
- **Primary Green:** `#059669` (Emerald 600) — Represents agriculture, health, and verified status.
- **Primary Hover:** `#047857` (Emerald 700).
- **Secondary Accent:** `#D97706` (Amber 600) — Represents indigenous cattle tones, warmth, and confidence indicators.
- **Background Base:** `#F8FAFC` (Slate 50) — Soft clean canvas reducing eye strain.
- **Card Background:** `#FFFFFF` (Pure White) with subtle box-shadows (`0 4px 6px -1px rgb(0 0 0 / 0.05)`).
- **Text Primary:** `#0F172A` (Slate 900) — High contrast readable text.
- **Text Muted:** `#64748B` (Slate 500) — Captions and secondary indicators.

### Typography
- **Headings:** Inter, system-ui, -apple-system, sans-serif (Font Weight: 700 / Bold).
- **Body:** Inter, sans-serif (Font Weight: 400 / Regular, 500 / Medium).
- **Confidence Scores & Metrics:** JetBrains Mono or tabular figures for numeric alignment.

---

## 3. Screen Structure & Layout Wireframes

```
+---------------------------------------------------------------------------------------+
|  [CB Logo] BreedWise  | Indian Livestock Recognition        [● FastAPI Connected]     |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|   HERO SECTION                                                                        |
|   AI-Powered Livestock Identification                                                 |
|   "Recognise the breed. Preserve our indigenous heritage."                            |
|   [SDG 2 Zero Hunger]  [EfficientNet-B0 Backbone]  [14 Indian Breeds]                 |
|                                                                                       |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|   WORKSPACE (2 Columns on Desktop, Single Column on Mobile)                          |
|                                                                                       |
|   +--------------------------------------+  +-------------------------------------+   |
|   | 01. UPLOAD ANIMAL PHOTO              |  | 02. RECOGNITION RESULTS             |   |
|   | Select animal category:              |  | Top Identified Breed:               |   |
|   | [ (🐄) Cattle ]  [ (🐃) Buffalo ]    |  | +---------------------------------+ |   |
|   |                                      |  | | Gir Cattle (Gujarat)     [94.2%] | |   |
|   | +----------------------------------+ |  | +---------------------------------+ |   |
|   | |      [Drag & Drop Image]         | |  |                                     |   |
|   | |               or                 | |  | Confidence Bar: [==========      ] |   |
|   | |      [Browse Files (5MB max)]    | |  |                                     |   |
|   | |       JPEG, PNG, WEBP            | |  | Top Candidates:                     |   |
|   | +----------------------------------+ |  |  1. Gir            94.2%            |   |
|   |                                      |  |  2. Sahiwal         3.9%            |   |
|   | Quick Samples:                       |  |  3. Red Sindhi      1.2%            |   |
|   | [Gir] [Sahiwal] [Murrah] [Jaffrabadi]|  |                                     |   |
|   |                                      |  | Breed Profile:                      |   |
|   | [Identify Breed Button]              |  | • Origin: Saurashtra, Gujarat       |   |
|   |                                      |  | • Milk Yield: 10 - 15 Litres/Day    |   |
|   |                                      |  | • Primary Use: Dairy                |   |
|   +--------------------------------------+  +-------------------------------------+   |
|                                                                                       |
+---------------------------------------------------------------------------------------+
|   03. RECENT IDENTIFICATION HISTORY TABLE                                             |
|   [Timestamp]       [Filename]          [Predicted Breed]     [Confidence]  [Status]  |
+---------------------------------------------------------------------------------------+
|   FOOTER: SKIT Jaipur · CSE (AI) · Academic Session 2026-27                           |
+---------------------------------------------------------------------------------------+
```

---

## 4. User Interaction Flow
1. **Entry**: User lands on the page. Active connection status to FastAPI is displayed in the navigation bar.
2. **Category Selection**: User chooses between Cattle or Buffalo (pre-filters test samples).
3. **Image Ingestion**:
   - Drag and drop image onto dropzone, or
   - Click "Browse Files" to open native file selector, or
   - Select a quick demo sample.
4. **Validation Check**: File format verified (`.jpg`, `.jpeg`, `.png`, `.webp`) and size capped at `< 5MB`. Invalid files trigger an inline warning banner.
5. **Execution**: User clicks "Identify Breed". Dropzone switches to animated scanning state.
6. **Result Presentation**: Results panel reveals the top predicted breed, confidence meter, top-3 candidates, and full breed dossier.
7. **History Update**: The prediction is logged to the local and database history table.
