import React from 'react';
import { SafeAreaView, Text, View, Pressable } from 'react-native';

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

export default function App() {
  return (
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
}

