import React, { useState } from 'react';
import { View, Text, Button, FlatList, StyleSheet, Slider } from 'react-native';
import axios from 'axios';

const MealPlanScreen = ({ onBack }) => {
  const [budget, setBudget] = useState(500);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPlan = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/plan', {
        budget: budget
      });
      setPlan(response.data.plan);
    } catch (err) {
      setError(err.response?.data?.message || "Failed to generate plan");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Meal Planner</Text>

      <View style={styles.controls}>
        <Text>Daily Budget: {budget} NOK</Text>
        <Slider
          style={{width: '100%', height: 40}}
          minimumValue={100}
          maximumValue={2000}
          step={50}
          value={budget}
          onValueChange={setBudget}
        />
        <Button title="Generate Plan" onPress={fetchPlan} disabled={loading} />
      </View>

      {error && <Text style={styles.error}>{error}</Text>}

      {plan && (
        <View style={styles.result}>
          <Text style={styles.summary}>Total Calories: {plan.total_calories}</Text>
          <Text style={styles.summary}>Total Cost: {plan.total_cost.toFixed(2)} NOK</Text>
          <Text style={styles.summary}>Urgency Score: {plan.total_urgency_score.toFixed(1)}</Text>

          <FlatList
            data={plan.meals}
            keyExtractor={(item, index) => index.toString()}
            renderItem={({item, index}) => (
              <View style={styles.mealItem}>
                <Text style={styles.mealName}>Meal {index + 1}: {item}</Text>
              </View>
            )}
          />
        </View>
      )}

      <Button title="Back to Pantry" onPress={onBack} color="#888" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
    paddingTop: 50,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  controls: {
    marginBottom: 20,
    padding: 10,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
  },
  error: {
    color: 'red',
    marginBottom: 10,
    textAlign: 'center',
  },
  result: {
    flex: 1,
    marginBottom: 20,
  },
  summary: {
    fontSize: 16,
    marginBottom: 5,
  },
  mealItem: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  mealName: {
    fontSize: 18,
    fontWeight: '500',
  },
});

export default MealPlanScreen;
