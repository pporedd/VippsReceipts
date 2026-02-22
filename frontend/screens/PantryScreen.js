import React, { useState, useEffect } from 'react';
import { View, Text, Image, Button, StyleSheet, Dimensions } from 'react-native';
import Swiper from 'react-native-deck-swiper';
import axios from 'axios';

const SCREEN_WIDTH = Dimensions.get('window').width;

const PantryScreen = ({ user, onPlanRequest }) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPantry();
  }, []);

  const fetchPantry = async () => {
    try {
      // Replace localhost with your machine's IP if testing on real device
      const response = await axios.get('http://127.0.0.1:5000/api/pantry');
      setItems(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Failed to fetch pantry", error);
    }
  };

  const onSwiped = (cardIndex, direction) => {
    const item = items[cardIndex];
    const action = direction === 'right' ? 'keep' : 'discard';

    // Simulate API call for FL
    axios.post('http://127.0.0.1:5000/api/swipe', {
      item_name: item.name,
      action: action
    }).catch(e => console.error("Failed to log swipe", e));
  };

  if (loading) return <Text>Loading Pantry...</Text>;

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Pantry (Sort: Expiring Soon)</Text>

      <View style={styles.cardContainer}>
        {items.length > 0 ? (
          <Swiper
            cards={items}
            renderCard={(card) => {
              // Handle potential empty card at end
              if (!card) return <View />;

              // Color border based on urgency
              const urgencyColor = card.days_left < 3 ? 'red' : (card.days_left < 7 ? 'orange' : 'green');

              return (
                <View style={[styles.card, { borderColor: urgencyColor, borderWidth: 4 }]}>
                  <Text style={styles.cardTitle}>{card.name}</Text>
                  <Text style={styles.cardText}>Expires in: {card.days_left} days</Text>
                  <Text style={styles.cardText}>{card.quantity} {card.unit}</Text>
                  <Image
                    source={{uri: card.image_url}}
                    style={styles.image}
                  />
                  <Text style={styles.hint}>Swipe RIGHT to Keep</Text>
                  <Text style={styles.hint}>Swipe LEFT to Discard</Text>
                </View>
              )
            }}
            onSwipedLeft={(index) => onSwiped(index, 'left')}
            onSwipedRight={(index) => onSwiped(index, 'right')}
            cardIndex={0}
            backgroundColor={'#f0f0f0'}
            stackSize= {3}
          />
        ) : (
          <Text>No items in pantry!</Text>
        )}
      </View>

      <Button title="Generate Meal Plan" onPress={onPlanRequest} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0f0f0',
    paddingTop: 50,
  },
  header: {
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  cardContainer: {
    flex: 1,
    height: 400, // Fixed height for swiper area
  },
  card: {
    flex: 0.7,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#E8E8E8',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'white',
    padding: 20,
  },
  cardTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  cardText: {
    fontSize: 18,
    marginBottom: 5,
  },
  image: {
    width: 200,
    height: 200,
    marginVertical: 20,
    borderRadius: 10
  },
  hint: {
    color: '#888',
    marginTop: 10,
    fontSize: 12
  }
});

export default PantryScreen;
