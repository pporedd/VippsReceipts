# Smart Pantry & Meal Planner Prototype

This project consists of a Python Flask backend (optimization logic) and a React Native Expo frontend (mobile UI).

## 1. Backend Setup

The backend handles the "Smart Pantry" logic, including:
- Ingesting receipts (mocked).
- Prioritizing ingredients by expiration date.
- Generating meal plans using Dynamic Programming.

### Prerequisites
- Python 3.x
- `pip install flask flask-cors requests`

### Running the Server
```bash
# From the root directory
python3 backend/app.py
```
The server will start on `http://127.0.0.1:5000`.

## 2. Frontend Setup

The frontend is a React Native app using Expo.

### Prerequisites
- Node.js & npm
- Expo CLI (`npm install -g expo-cli`)
- Expo Go app on your phone (iOS/Android)

### Installation
```bash
cd frontend
npm install
```

### Running the App
```bash
# Start the Expo development server
npx expo start
```
1. Scan the QR code with your phone (Android) or Camera app (iOS).
2. Ensure your phone and computer are on the **same Wi-Fi network**.
3. **Important:** Open `frontend/screens/PantryScreen.js` and `frontend/screens/MealPlanScreen.js` and replace `127.0.0.1` with your computer's local IP address (e.g., `192.168.1.5`).

## 3. Features

1.  **Login:** Simulates Vipps login.
2.  **Pantry Swipe:**
    -   Shows ingredients expiring soonest first.
    -   **Swipe Right** to Keep.
    -   **Swipe Left** to Discard.
    -   Border color changes based on urgency (Red = <3 days).
3.  **Meal Planner:**
    -   Adjust daily budget.
    -   Click "Generate Plan" to get a recipe combination that fits your calories and budget while using up expiring food.
