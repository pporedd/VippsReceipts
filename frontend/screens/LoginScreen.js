import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, TouchableOpacity } from 'react-native';

const LoginScreen = ({ onLogin }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Smart Pantry</Text>
      <TouchableOpacity
        style={styles.button}
        onPress={onLogin}
      >
        <Text style={styles.buttonText}>Log in with Vipps</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 40,
    color: '#ff5b24', // Vipps-like orange
  },
  button: {
    backgroundColor: '#ff5b24',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default LoginScreen;
