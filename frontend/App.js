import React, { useState } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import LoginScreen from './screens/LoginScreen';
import PantryScreen from './screens/PantryScreen';
import MealPlanScreen from './screens/MealPlanScreen';

export default function App() {
  const [screen, setScreen] = useState('login');
  const [user, setUser] = useState(null);

  const handleLogin = async () => {
    try {
      // Simulate login
      const response = await fetch('http://127.0.0.1:5000/api/login', { method: 'POST' });
      const data = await response.json();
      if (data.status === 'success') {
        setUser(data.user);
        setScreen('pantry');
      }
    } catch (e) {
      console.error("Login failed", e);
      alert("Make sure Backend is running on Port 5000!");
    }
  };

  const renderScreen = () => {
    switch(screen) {
      case 'login':
        return <LoginScreen onLogin={handleLogin} />;
      case 'pantry':
        return <PantryScreen user={user} onPlanRequest={() => setScreen('plan')} />;
      case 'plan':
        return <MealPlanScreen onBack={() => setScreen('pantry')} />;
      default:
        return <LoginScreen />;
    }
  };

  return (
    <View style={styles.container}>
      {renderScreen()}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
