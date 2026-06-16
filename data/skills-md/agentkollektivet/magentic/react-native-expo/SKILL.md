---
name: react-native-expo
description: React Native and Expo development context skill. Covers mobile-specific patterns, navigation, native modules, platform differences, and wraps official Expo plugins for SDK upgrades, UI components, deployment, and CI/CD.
---

# React Native & Expo

Context skill for building mobile applications with React Native and Expo, including mobile-specific patterns and integration with official Expo plugins.

## External Dependencies

This skill wraps and coordinates with official Expo plugins. Install them for full functionality:

- `upgrading-expo` — SDK version upgrades and dependency fixes
- `expo-app-design` — UI components (SwiftUI, Jetpack Compose, Tailwind, DOM components)
- `expo-deployment` — App Store, Play Store, and web deployment
- `expo-app-design:expo-api-routes` — API routes with EAS Hosting
- `expo-deployment:expo-cicd-workflows` — EAS CI/CD workflow configuration

## Mobile-Specific Patterns

### Navigation (Expo Router)

```typescript
// app/_layout.tsx — Root layout with tabs
import { Tabs } from 'expo-router'

export default function RootLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: 'Home' }} />
      <Tabs.Screen name="search" options={{ title: 'Search' }} />
      <Tabs.Screen name="profile" options={{ title: 'Profile' }} />
    </Tabs>
  )
}
```

### Platform-Specific Code

```typescript
import { Platform } from 'react-native'

const styles = {
  container: {
    paddingTop: Platform.OS === 'ios' ? 44 : 0,
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 } },
      android: { elevation: 4 },
    }),
  },
}
```

### Safe Area Handling

```typescript
import { SafeAreaView } from 'react-native-safe-area-context'

export function Screen({ children }: { children: React.ReactNode }) {
  return (
    <SafeAreaView style={{ flex: 1 }} edges={['top', 'bottom']}>
      {children}
    </SafeAreaView>
  )
}
```

### Responsive Dimensions

```typescript
import { useWindowDimensions } from 'react-native'

export function ResponsiveGrid({ items }: { items: Item[] }) {
  const { width } = useWindowDimensions()
  const columns = width > 768 ? 3 : width > 480 ? 2 : 1

  return (
    <FlatList
      data={items}
      numColumns={columns}
      key={columns}
      renderItem={({ item }) => (
        <View style={{ width: width / columns }}>
          <ItemCard item={item} />
        </View>
      )}
    />
  )
}
```

## Performance

### FlatList Optimization

```typescript
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={item => item.id}
  getItemLayout={(_, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  maxToRenderPerBatch={10}
  windowSize={5}
  removeClippedSubviews={true}
  initialNumToRender={10}
/>
```

### Image Optimization

```typescript
import { Image } from 'expo-image'

<Image
  source={{ uri: imageUrl }}
  style={{ width: 200, height: 200 }}
  contentFit="cover"
  placeholder={blurhash}
  transition={200}
/>
```

### Memoization

```typescript
const MemoizedCard = React.memo(({ item }: { item: Item }) => (
  <View>
    <Text>{item.name}</Text>
  </View>
))
```

## Data Fetching

```typescript
import { useQuery } from '@tanstack/react-query'

export function useItems() {
  return useQuery({
    queryKey: ['items'],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/items`)
      if (!response.ok) throw new Error('Failed to fetch')
      return response.json()
    },
    staleTime: 5 * 60 * 1000,
  })
}
```

## Offline Support

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage'

async function getCachedData<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
  try {
    const data = await fetcher()
    await AsyncStorage.setItem(key, JSON.stringify(data))
    return data
  } catch {
    const cached = await AsyncStorage.getItem(key)
    if (cached) return JSON.parse(cached)
    throw new Error('No data available offline')
  }
}
```

## Push Notifications

```typescript
import * as Notifications from 'expo-notifications'

async function registerForPushNotifications() {
  const { status } = await Notifications.requestPermissionsAsync()
  if (status !== 'granted') return null

  const token = await Notifications.getExpoPushTokenAsync()
  return token.data
}
```

## Animations

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated'

export function AnimatedCard() {
  const scale = useSharedValue(1)

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: withSpring(scale.value) }],
  }))

  return (
    <Pressable
      onPressIn={() => { scale.value = 0.95 }}
      onPressOut={() => { scale.value = 1 }}
    >
      <Animated.View style={animatedStyle}>
        <Text>Press me</Text>
      </Animated.View>
    </Pressable>
  )
}
```

## Testing Mobile Apps

### Unit Tests
```typescript
import { render, fireEvent } from '@testing-library/react-native'

test('button calls onPress', () => {
  const onPress = jest.fn()
  const { getByText } = render(<Button onPress={onPress}>Tap</Button>)

  fireEvent.press(getByText('Tap'))
  expect(onPress).toHaveBeenCalledTimes(1)
})
```

### E2E with Detox or Maestro
```yaml
# maestro/flow.yaml
appId: com.example.app
---
- launchApp
- tapOn: "Search"
- inputText: "test query"
- assertVisible: "Results"
```

## Common Pitfalls

1. **Don't use `ScrollView` for long lists** — Use `FlatList` or `FlashList`
2. **Don't block the JS thread** — Use `InteractionManager` for heavy work
3. **Don't forget keyboard handling** — Use `KeyboardAvoidingView`
4. **Test on real devices** — Simulators miss performance and permission issues
5. **Handle deep links** — Configure universal links and app links
6. **Respect platform conventions** — iOS bottom sheets vs Android bottom navigation

## Project Structure

```
app/
  _layout.tsx         # Root layout
  (tabs)/
    _layout.tsx       # Tab navigation
    index.tsx         # Home tab
    search.tsx        # Search tab
    profile.tsx       # Profile tab
  [id].tsx            # Dynamic route
components/
  ItemCard.tsx
  SearchBar.tsx
hooks/
  useItems.ts
lib/
  api.ts
  storage.ts
constants/
  colors.ts
  layout.ts
```

Build mobile apps that feel native on each platform. Use Expo's managed workflow for fast iteration, eject only when necessary.
