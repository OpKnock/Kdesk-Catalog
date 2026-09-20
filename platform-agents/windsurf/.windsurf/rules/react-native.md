---
trigger: glob
description: "React Native mobile development. Real react-native CLI."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# mobile-react-native

React Native mobile development. Real react-native CLI.

## Instructions

# React Native

React Native mobile development using real CLI.

## When to Use

- Cross-platform mobile apps
- iOS and Android development

## Commands

```bash
# Create project
npx react-native init MyApp

# Run iOS
npx react-native run-ios

# Run Android
npx react-native run-android

# Start Metro
npx react-native start

# Build iOS release
cd ios && xcodebuild -scheme MyApp -configuration Release

# Build Android release
cd android && ./gradlew assembleRelease

# Run tests
npx jest

# Lint
npx eslint src/
```

## Component

```tsx
// src/components/UserCard.tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface UserCardProps {
  name: string;
  email: string;
}

export const UserCard = ({ name, email }: UserCardProps) => {
  return (
    <View style={styles.card}>
      <Text style={styles.name}>{name}</Text>
      <Text style={styles.email}>{email}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    padding: 16,
    margin: 8,
    backgroundColor: '#fff',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2
  },
  name: {
    fontSize: 18,
    fontWeight: 'bold'
  },
  email: {
    fontSize: 14,
    color: '#666'
  }
});
```

## Navigation

```tsx
// src/App.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from './screens/HomeScreen';
import DetailScreen from './screens/DetailScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Detail" component={DetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## State Management

```tsx
// src/store/authSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }) => {
    const response = await fetch('https://api.example.com/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    return response.json();
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null, loading: false },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => { state.loading = true; })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      });
  }
});
```

## Capabilities

### mobile-react-native
React Native mobile development. Real react-native CLI.

**Commands:**
- `npx react-native init MyApp`
- `npx react-native run-ios`
- `npx react-native run-android`
- `npx react-native start`
- `cd ios && xcodebuild -scheme MyApp -configuration Release`
- `cd android && ./gradlew assembleRelease`
- `npx jest`
- `npx eslint src/`

**Examples:**
- npx react-native init MyApp
- npx react-native run-ios
- npx react-native run-android
