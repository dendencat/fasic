import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { SafeAreaView, Text, View, Pressable, PanGestureHandler, State } from 'react-native';
import { PanGestureHandlerGestureEvent, PanGestureHandlerStateChangeEvent, State as GestureState } from 'react-native-gesture-handler';

const Stack = createStackNavigator();

const ControlButton = ({ label }: { label: string }) => (
  <Pressable
    style={({ pressed }) => ({
      backgroundColor: pressed ? '#1f2937' : '#111827',
      paddingVertical: 12,
      paddingHorizontal: 16,
      borderRadius: 8,
      marginHorizontal: 6,
    })}
    onPress={() => {}}
  >
    <Text style={{ color: '#e5e7eb', fontWeight: '600' }}>{label}</Text>
  </Pressable>
);

const HomeScreen = () => (
  <SafeAreaView style={{ flex: 1, backgroundColor: '#0f172a' }}>
    <View style={{ padding: 20 }}>
      <Text style={{ color: '#e5e7eb', fontSize: 28, fontWeight: '700' }}>SwipeTune</Text>
      <Text style={{ color: '#94a3b8', marginTop: 8 }}>Hello — 再生UIの枠</Text>
    </View>

    <View
      style={{
        marginTop: 24,
        marginHorizontal: 20,
        padding: 16,
        backgroundColor: '#0b1220',
        borderRadius: 12,
        borderWidth: 1,
        borderColor: '#1f2937',
      }}
    >
      <Text style={{ color: '#cbd5e1', marginBottom: 12 }}>Now Playing: (dummy)</Text>
      <View style={{ flexDirection: 'row', justifyContent: 'center' }}>
        <ControlButton label="Prev" />
        <ControlButton label="Play/Pause" />
        <ControlButton label="Next" />
      </View>
    </View>
  </SafeAreaView>
);

const ExploreScreen = () => {
  const onGestureEvent = (event: PanGestureHandlerGestureEvent) => {
    // Handle swipe
  };

  const onHandlerStateChange = (event: PanGestureHandlerStateChangeEvent) => {
    if (event.nativeEvent.state === GestureState.END) {
      // Determine like/dislike
    }
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#0f172a', justifyContent: 'center', alignItems: 'center' }}>
      <Text style={{ color: '#e5e7eb', fontSize: 24 }}>Explore Screen</Text>
      <PanGestureHandler onGestureEvent={onGestureEvent} onHandlerStateChange={onHandlerStateChange}>
        <View style={{ width: 300, height: 400, backgroundColor: '#1f2937', borderRadius: 12, justifyContent: 'center', alignItems: 'center' }}>
          <Text style={{ color: '#e5e7eb' }}>Swipe Card</Text>
        </View>
      </PanGestureHandler>
    </SafeAreaView>
  );
};

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Explore" component={ExploreScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

