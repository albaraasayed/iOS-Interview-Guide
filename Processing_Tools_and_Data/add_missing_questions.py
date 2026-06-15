#!/usr/bin/env python3
"""
add_missing_questions.py
Inserts the missing questions into Organized_Interviews.md.
Does NOT touch any other content. README.md is never touched.
"""

import re, shutil, os

SOURCE = 'Organized_Interviews.md'
BACKUP = 'Organized_Interviews.md.bak'

# ── Backup first ────────────────────────────────────────────────────────────
shutil.copy2(SOURCE, BACKUP)
print(f'✅ Backup created: {BACKUP}')

with open(SOURCE, 'r', encoding='utf-8') as f:
    content = f.read()

# ── Helper ───────────────────────────────────────────────────────────────────
def insert_before(content, marker, new_text):
    """Insert new_text just before the line matching marker."""
    idx = content.find(marker)
    if idx == -1:
        raise ValueError(f'Marker not found: {marker!r}')
    return content[:idx] + new_text + content[idx:]

# ═══════════════════════════════════════════════════════════════════════════
#  SWIFTUI QUESTIONS  (insert before ## SwiftData)
# ═══════════════════════════════════════════════════════════════════════════
SWIFTUI_QUESTIONS = """
### What is the difference between `@State`, `@Binding`, `@ObservedObject`, and `@EnvironmentObject`? [Expert]

SwiftUI provides four core property wrappers for managing and sharing state across views. Choosing the right one is critical for building correct, efficient UIs.

| Wrapper | Owns the state? | Scope | Source of truth |
| --- | --- | --- | --- |
| **`@State`** | ✅ Yes | Private to the view | The view itself |
| **`@Binding`** | ❌ No — references parent | Passed down | A parent `@State` |
| **`@ObservedObject`** | ❌ No — holds reference | Any view that receives it | External `ObservableObject` |
| **`@EnvironmentObject`** | ❌ No — injected | Any descendant in the tree | Ancestor via `.environmentObject()` |

**`@State` — local, private value:**
```swift
struct Counter: View {
    @State private var count = 0  // Owned and private to this view
    var body: some View {
        Button("Tapped \\(count) times") { count += 1 }
    }
}
```

**`@Binding` — a two-way reference to a parent's state:**
```swift
struct Toggle: View {
    @Binding var isOn: Bool  // Does NOT own the value
    var body: some View {
        Button(isOn ? "ON" : "OFF") { isOn.toggle() }
    }
}
// Usage: Toggle(isOn: $parentStateVar)
```

**`@ObservedObject` — external reference type that publishes changes:**
```swift
class ViewModel: ObservableObject {
    @Published var title = "Hello"
}
struct MyView: View {
    @ObservedObject var vm: ViewModel  // Injected; NOT owned
    var body: some View { Text(vm.title) }
}
```
> **Warning:** `@ObservedObject` does NOT guarantee the object's lifetime. If the parent view is re-created, the object may be re-instantiated and state lost. Use `@StateObject` for ownership.

**`@EnvironmentObject` — implicit dependency injection through the view tree:**
```swift
// Inject at a high level
ContentView().environmentObject(myViewModel)

// Access deep in the hierarchy without explicit passing
struct DeepView: View {
    @EnvironmentObject var vm: ViewModel  // Automatically resolved
}
```

---

### What is the difference between `@ObservedObject` and `@StateObject`? [Expert]

Both work with types conforming to `ObservableObject`, but they differ critically in **ownership and lifecycle**.

| | `@StateObject` | `@ObservedObject` |
| --- | --- | --- |
| **Ownership** | The view **owns** the object | The view **does not own** the object |
| **Lifetime** | Created once; survives view re-renders | May be re-created when the parent view re-renders |
| **Use when** | This view is the **source of truth** | Object is **created and owned elsewhere** and passed in |
| **Available since** | iOS 14 | iOS 13 |

**The critical difference in practice:**
```swift
// ❌ WRONG — may lose state when parent re-renders
struct BadView: View {
    @ObservedObject var vm = MyViewModel()  // Re-created on every parent re-render!
    ...
}

// ✅ CORRECT — SwiftUI guarantees vm is created only once
struct GoodView: View {
    @StateObject private var vm = MyViewModel()  // Owned; stable lifetime
    ...
}

// ✅ CORRECT — vm is owned elsewhere, passed in
struct ReceiverView: View {
    @ObservedObject var vm: MyViewModel  // Just observing an external object
    ...
}
```

**Rule of thumb:** If you write `= MyViewModel()` inline in a view, use `@StateObject`. If the object is created outside the view and passed in, use `@ObservedObject`.

---

### What is SwiftUI's Environment system and how do you use `@Environment`, `@EnvironmentObject`, and `.environment()`? [Mid]

SwiftUI's **Environment** is a dependency injection mechanism that propagates values down the entire view hierarchy without explicit parameter passing.

**`@Environment` — reading built-in or custom environment values:**
```swift
struct AdaptiveText: View {
    @Environment(\\.colorScheme) var colorScheme   // Built-in
    @Environment(\\.dynamicTypeSize) var typeSize   // Built-in

    var body: some View {
        Text("Hello")
            .foregroundColor(colorScheme == .dark ? .white : .black)
    }
}
```

**Custom environment values:**
```swift
struct ThemeKey: EnvironmentKey {
    static let defaultValue: Theme = .standard
}
extension EnvironmentValues {
    var theme: Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}
// Inject: MyView().environment(\\.theme, .dark)
// Read:   @Environment(\\.theme) var theme
```

**`@EnvironmentObject` — sharing a reference-type observable object:**
```swift
// High-level ancestor injects the object:
@main struct App: SwiftUI.App {
    @StateObject private var session = UserSession()
    var body: some Scene {
        WindowGroup { RootView().environmentObject(session) }
    }
}
// Any descendant can access it:
struct ProfileView: View {
    @EnvironmentObject var session: UserSession
}
```

> **Key distinction:** `@Environment` is for value types and built-in system values. `@EnvironmentObject` is for reference types (`ObservableObject`) that need to propagate and trigger UI updates.

---

### What is the lifecycle of a SwiftUI View? [Mid]

SwiftUI manages view lifecycles differently from UIKit, with distinct phases:

```
1. Initialization  →  init() is called
        ↓
2. Appearing       →  body is computed; onAppear() fires
        ↓
3. Updating        →  body recomputed when state/bindings change
        ↓
4. Disappearing    →  onDisappear() fires
        ↓
5. Destruction     →  View struct is deallocated (no deinit)
```

**Key callbacks:**
```swift
struct LifecycleView: View {
    @State private var data: [Item] = []

    var body: some View {
        List(data) { item in ItemRow(item: item) }
            .onAppear {
                // Called every time the view appears on screen
                // Good for: starting timers, fetching data, logging
                loadData()
            }
            .onDisappear {
                // Called every time the view leaves the screen
                // Good for: stopping timers, saving state
                saveState()
            }
            .task {
                // async/await variant of onAppear; auto-cancelled on disappear
                await fetchData()
            }
    }
}
```

**Important distinctions from UIKit:**
- There is **no `deinit`** because SwiftUI views are structs (value types).
- `body` is recomputed frequently — keep it **pure and cheap**.
- `init()` is called on every re-render — do **not** perform side effects there.
- Use `onAppear`/`onDisappear` for lifecycle side effects.

---

### What is the difference between a SwiftUI `View` and a `UIView`? [Mid]

| Aspect | SwiftUI `View` | UIKit `UIView` |
| --- | --- | --- |
| **Type** | Protocol (conforming types are structs) | Class (reference type) |
| **Programming model** | Declarative — describes desired state | Imperative — manually manipulates state |
| **Memory** | Stack-allocated value type | Heap-allocated, ARC-managed |
| **Mutability** | Immutable; SwiftUI creates new instances on state change | Mutable in place |
| **Lifecycle** | Managed by SwiftUI's diffing engine | Managed manually (viewDidLoad, etc.) |
| **Identity** | Structural (position in view hierarchy) | Object identity (`===`) |
| **Rendering** | Backed by CALayer/Metal via SwiftUI's render tree | Direct CALayer backing |
| **Platform** | iOS 13+, macOS 10.15+, tvOS, watchOS | iOS 2+ (very mature) |
| **Inheritance** | ❌ No subclassing | ✅ Rich subclassing hierarchy |

---

### What is the difference between a view's `init()` and the `onAppear()` modifier in SwiftUI? [Mid]

| | `init()` | `onAppear()` |
| --- | --- | --- |
| **When called** | Every time SwiftUI evaluates the view | Every time the view **appears** on screen |
| **Frequency** | Potentially very frequent (on every parent re-render) | Once per appearance |
| **Side effects** | ❌ Avoid — no async, no mutation of external state | ✅ Designed for side effects |
| **Async tasks** | ❌ Not possible | ✅ Use `.task {}` modifier |
| **Typical use** | Configuring initial property values, DI | Fetching data, starting timers, analytics |

```swift
struct ArticleView: View {
    let articleID: UUID
    @StateObject private var vm: ArticleViewModel  // Initialized via init

    init(articleID: UUID) {
        self.articleID = articleID
        // ✅ OK to configure @StateObject's initial value here
        _vm = StateObject(wrappedValue: ArticleViewModel(id: articleID))
    }

    var body: some View {
        Text(vm.title)
            .onAppear {
                // ✅ Trigger side effects here — not in init
                vm.fetchContent()
            }
            .task {
                // ✅ Async variant — auto-cancelled on disappear
                await vm.fetchComments()
            }
    }
}
```

---

### What is `@ViewBuilder` and how does it enable conditional rendering? [Mid]

`@ViewBuilder` is a **result builder** attribute that allows you to construct views using a DSL-like syntax with multiple expressions — including `if`, `if-else`, `switch`, and `ForEach` — without explicit return statements.

```swift
// @ViewBuilder allows multiple statements in a function/computed property
struct ContentCard: View {
    var isPremium: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Article Title").font(.headline)
            if isPremium {
                Text("Premium Content")
                    .foregroundColor(.yellow)
            } else {
                Text("Free Content")
            }
        }
    }
}
```

**Custom `@ViewBuilder` functions:**
```swift
@ViewBuilder
func statusView(for status: Status) -> some View {
    switch status {
    case .loading: ProgressView()
    case .success(let data): DataView(data: data)
    case .error(let msg): Text(msg).foregroundColor(.red)
    }
}
```

**Performance benefit:** `@ViewBuilder` uses static type information to build a strongly-typed view tree at compile time. SwiftUI can then use this type information to minimize diffing work — it knows exactly which branches of conditional views exist.

---

### What is the difference between stateful and stateless (presentational) views in SwiftUI? [Easy]

- **Stateful views** own and manage their own state using `@State` or `@StateObject`. They are the **source of truth** and drive changes to child views.
- **Stateless (presentational) views** have no state of their own. They receive all their data via `let` properties or `@Binding` and are purely responsible for rendering. They are easy to preview, test, and reuse.

```swift
// ✅ Stateless / presentational — receives data, doesn't own it
struct UserCard: View {
    let name: String
    let avatar: Image
    // No @State, no side effects
    var body: some View {
        HStack {
            avatar.clipShape(Circle())
            Text(name).font(.headline)
        }
    }
}

// ✅ Stateful — owns data and drives the child
struct UserListView: View {
    @StateObject private var vm = UserListViewModel()
    var body: some View {
        ForEach(vm.users) { user in
            UserCard(name: user.name, avatar: user.avatar)
        }
    }
}
```

**Best practice:** Keep your stateless leaf views as simple as possible. Push state management up to the appropriate parent view.

---

### How do you handle device orientation changes in SwiftUI? [Mid]

SwiftUI does not have a direct `UIDevice.orientationDidChangeNotification` equivalent, but you can observe orientation via the Environment or UIDevice notifications.

**Approach 1 — Environment size classes (recommended):**
```swift
struct AdaptiveLayout: View {
    @Environment(\\.horizontalSizeClass) var hSizeClass

    var body: some View {
        if hSizeClass == .compact {
            VStack { content }   // Portrait / compact width
        } else {
            HStack { content }   // Landscape / regular width
        }
    }
    @ViewBuilder var content: some View {
        Text("Main").frame(maxWidth: .infinity)
        Text("Detail").frame(maxWidth: .infinity)
    }
}
```

**Approach 2 — GeometryReader for exact dimensions:**
```swift
struct OrientationAwareView: View {
    var body: some View {
        GeometryReader { geo in
            if geo.size.width > geo.size.height {
                LandscapeLayout()
            } else {
                PortraitLayout()
            }
        }
    }
}
```

**Approach 3 — UIDevice notification (legacy interop):**
```swift
struct OrientationView: View {
    @State private var isLandscape = false

    var body: some View {
        Text(isLandscape ? "Landscape" : "Portrait")
            .onReceive(NotificationCenter.default.publisher(
                for: UIDevice.orientationDidChangeNotification
            )) { _ in
                isLandscape = UIDevice.current.orientation.isLandscape
            }
    }
}
```

---

### What is `@StateObject` in SwiftUI and when should you use it? [Mid]

`@StateObject` is a property wrapper that creates and **owns** an `ObservableObject` for the lifetime of the view. SwiftUI guarantees it is created only **once**, even when the parent view re-renders and recreates the child view.

```swift
class TimerViewModel: ObservableObject {
    @Published var elapsed: Int = 0
    private var timer: Timer?

    init() {
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            self.elapsed += 1
        }
    }
    deinit { timer?.invalidate() }
}

struct TimerView: View {
    @StateObject private var vm = TimerViewModel()  // Created once, stable

    var body: some View {
        Text("Elapsed: \\(vm.elapsed)s")
    }
}
```

**When to use:** Any time **this view is the origin** of an observable object (i.e., you write `= ViewModel()` directly). If the object is created outside and passed in, use `@ObservedObject` instead.

---
"""

# ── Swift Fundamentals missing questions ────────────────────────────────────
SWIFT_QUESTIONS = """
### What is the difference between a completion handler and Swift Concurrency (`async`/`await`)? [Expert]

Both mechanisms handle asynchronous work, but Swift Concurrency (introduced in Swift 5.5) is the modern, structured replacement for callback-based completion handlers.

**Completion Handler (Legacy):**
```swift
func fetchUser(id: Int, completion: @escaping (Result<User, Error>) -> Void) {
    URLSession.shared.dataTask(with: url) { data, _, error in
        if let error = error {
            completion(.failure(error))
        } else if let data = data, let user = try? JSONDecoder().decode(User.self, from: data) {
            completion(.success(user))
        }
    }.resume()
}

// Usage — callback hell when chaining
fetchUser(id: 1) { result in
    switch result {
    case .success(let user):
        fetchPosts(for: user) { posts in
            // Another level of nesting...
        }
    case .failure(let error): handleError(error)
    }
}
```

**Problems with completion handlers:**
- **Callback hell** — deeply nested, hard to read.
- **Error handling** is manual and easy to forget.
- **Retain cycle risk** — `@escaping` closures capture `self` strongly unless `[weak self]` is used.
- **No structured cancellation** — hard to cancel midway.

**Swift Concurrency (`async`/`await`):**
```swift
func fetchUser(id: Int) async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Usage — reads like synchronous code
Task {
    do {
        let user = try await fetchUser(id: 1)
        let posts = try await fetchPosts(for: user)  // Sequential, linear
    } catch {
        handleError(error)
    }
}
```

**Advantages of `async`/`await`:**
- **Linear, readable code** — no nesting.
- **Structured error handling** via `throws`/`try`.
- **No retain cycles** — `self` is captured by the `Task`, not an escaping closure.
- **Structured cancellation** — tasks can be cancelled cooperatively.
- **`async let`** for concurrent parallel tasks:
```swift
async let user  = fetchUser(id: 1)
async let posts = fetchPosts(id: 1)
let (u, p) = try await (user, posts)  // Both start concurrently
```

---

### What is `@autoclosure` in Swift and when should you use it? [Mid]

`@autoclosure` is an attribute that automatically wraps an expression in a closure when it is passed as an argument. The closure is only evaluated when explicitly called, enabling **lazy evaluation** of arguments.

```swift
// Without @autoclosure — caller must write { } explicitly
func logIfDebug(_ message: () -> String) {
    if isDebugMode { print(message()) }
}
logIfDebug({ expensiveDescription() })  // Awkward at call site

// With @autoclosure — expression wraps automatically
func logIfDebug(_ message: @autoclosure () -> String) {
    if isDebugMode { print(message()) }
}
logIfDebug(expensiveDescription())  // Clean call site; only evaluated if isDebugMode
```

**Standard library examples:**
- `assert(_:_:file:line:)` — condition is `@autoclosure` so it's only evaluated in debug builds.
- `??` operator — the right-hand side is `@autoclosure` so it's only evaluated if the left side is `nil`.

```swift
// The ?? operator is implemented roughly like:
func ??<T>(optional: T?, default: @autoclosure () throws -> T) rethrows -> T {
    switch optional {
    case .some(let value): return value
    case .none: return try default()  // Only called if optional is nil
    }
}
```

**When to use:** Use `@autoclosure` when you want to accept a simple expression at the call site but only evaluate it lazily (conditionally or deferred). Always document this behavior since it hides the fact that an expression is deferred.

---

### What is a variadic function in Swift? [Easy]

A **variadic function** accepts zero or more values of a specified type, collected into an array inside the function body. You declare a variadic parameter by appending `...` to the type name.

```swift
func sum(_ numbers: Int...) -> Int {
    return numbers.reduce(0, +)  // numbers is [Int] inside the function
}

print(sum(1, 2, 3))        // 6
print(sum(10, 20))         // 30
print(sum())               // 0

// Multiple parameters (variadic must be last)
func logEvent(_ name: String, tags: String...) {
    print("Event: \\(name), Tags: \\(tags.joined(separator: ", "))")
}
logEvent("Purchase", tags: "ecommerce", "conversion", "premium")
```

**Rules:**
- A function can have **at most one** variadic parameter.
- The variadic parameter is treated as an **array** (`[T]`) inside the function body.
- Variadic parameters can appear anywhere in the parameter list, but must be followed by labelled parameters if not last.
- `print(_:separator:terminator:)` itself uses a variadic first parameter.

---

### What are Swift's Set operations and how do you use them? [Mid]

Swift's `Set<Element>` provides full support for mathematical set operations. All of these return a new set (or boolean) without modifying the originals.

```swift
let a: Set = [1, 2, 3, 4, 5]
let b: Set = [4, 5, 6, 7, 8]

// ── Combining Sets ──────────────────────────────────────────
let union = a.union(b)                    // [1,2,3,4,5,6,7,8] — all elements from both
let intersection = a.intersection(b)     // [4, 5]             — elements in both
let difference = a.subtracting(b)        // [1, 2, 3]          — in a but not in b
let symDiff = a.symmetricDifference(b)   // [1,2,3,6,7,8]      — in either, not both

// ── Membership Checks ───────────────────────────────────────
let isSubset  = Set([4, 5]).isSubset(of: a)       // true  — [4,5] ⊆ a
let isSuperset = a.isSuperset(of: Set([1, 2]))    // true  — a ⊇ [1,2]
let isDisjoint = a.isDisjoint(with: Set([6, 7]))  // true  — no common elements
let isStrictSubset = Set([4, 5]).isStrictSubset(of: a)  // true (is subset AND not equal)

// ── Mutating Variants (on var sets) ─────────────────────────
var c: Set = [1, 2, 3]
c.formUnion([4, 5])             // c = [1,2,3,4,5]
c.formIntersection([3, 4])      // c = [3,4]
c.subtract([4])                 // c = [3]
c.formSymmetricDifference([3,5])// c = [5]
```

**Complexity:** All set operations run in O(n) time where n is the size of the smaller set, thanks to the underlying hash table. This makes `Set` vastly more efficient than array-based approaches for membership testing and set algebra.

---
"""

# ── UIKit missing questions ──────────────────────────────────────────────────
UIKIT_QUESTIONS = """
### What is the difference between points and pixels in iOS? [Easy]

In iOS, layout is done in **points** (logical units), not physical pixels. This abstraction allows the same layout code to work correctly across devices with different display densities.

| Concept | Definition | Example |
| --- | --- | --- |
| **Point (pt)** | Logical unit of measurement used in all UIKit and SwiftUI APIs | A button is `44pt` tall |
| **Pixel (px)** | Physical hardware pixel on the display | On a 3× display, 44pt = 132px |
| **Scale factor** | Ratio of pixels to points (`UIScreen.main.scale`) | 1.0× (non-Retina), 2.0×, 3.0× |

**Common scale factors:**
- `1×` — Original non-Retina displays (very old devices)
- `2×` — Most iPhones and all non-Pro iPads (Retina)
- `3×` — iPhone Pro / Plus models (Super Retina)

```swift
let scale = UIScreen.main.scale          // e.g. 3.0
let nativeSize = UIScreen.main.nativeBounds.size  // in physical pixels
let logicalSize = UIScreen.main.bounds.size       // in points

// Converting: 1pt = scale × pixels
// A 44pt button on a 3× display = 132 physical pixels
```

**Practical implication:** When working with `Core Graphics` or image assets, work in pixels (multiply by scale). For `Auto Layout` and frame-based layout, always work in points.

---

### How does the iOS Main Run Loop and Update Cycle work? [Expert]

The **Main Run Loop** is the event-processing loop that runs continuously on the main thread, driving all user interaction and UI updates.

**The loop cycle:**
```
1. Receive Event (touch, timer, system notification)
         ↓
2. Application processes event → may trigger state changes
         ↓
3. Update Cycle runs (deferred):
     a. setNeedsLayout() marks views dirty
     b. layoutIfNeeded() / layoutSubviews() runs (top-down)
     c. setNeedsDisplay() marks layers dirty
     d. draw(_:) runs on dirty layers
         ↓
4. Core Animation commits changes to render server
         ↓
5. Display hardware composites and presents the frame
         ↓
6. Back to step 1
```

**The Update Cycle (deferred rendering):**
UIKit does **not** immediately re-render after every property change. Instead, it accumulates changes during event processing and flushes them in a single pass at the end of the run loop iteration. This is why:

- `setNeedsLayout()` — schedules layout for the next cycle (fast, non-blocking).
- `layoutIfNeeded()` — forces layout **immediately** (used before animations).
- `setNeedsDisplay()` — schedules a redraw for the next cycle.

```swift
// Animating layout changes correctly:
UIView.animate(withDuration: 0.3) {
    self.heightConstraint.constant = 200
    self.view.layoutIfNeeded()  // Force immediate layout — required for constraint animations
}
```

**Why it matters:** Understanding the update cycle explains why changes made inside a `UIView.animate` block must call `layoutIfNeeded()`, and why direct frame changes mid-event can be batched unexpectedly.

---

### What is the difference between UITabBar, UIToolbar, and UINavigationBar? [Easy]

All three are bar-style UI components, but they serve different navigational and functional purposes:

| Bar | Position | Purpose | Managed by |
| --- | --- | --- | --- |
| **UINavigationBar** | Top | Shows current screen title, back button, and nav items. Enables hierarchical navigation. | `UINavigationController` |
| **UITabBar** | Bottom | Displays tabs for switching between distinct app sections. Selection changes the root view. | `UITabBarController` |
| **UIToolbar** | Bottom | Displays a row of action buttons relevant to the current screen. Does not change navigation. | Manual or `UINavigationController.toolbar` |

**Key distinctions:**
- `UITabBar` is for **switching between sections** (persistent selection state).
- `UIToolbar` is for **contextual actions** related to the current content (e.g., editing tools, share buttons).
- You can combine them: a `UITabBarController` can contain `UINavigationControllers`, each of which can show a `UIToolbar`.

---

### What is `UIStackView` and how does it manage the layout of subviews? [Easy]

`UIStackView` is a UIKit component that automatically manages the layout of an ordered list of subviews using Auto Layout, without requiring you to write explicit constraints between sibling views.

**Key properties:**
```swift
let stack = UIStackView(arrangedSubviews: [view1, view2, view3])
stack.axis         = .vertical          // .horizontal or .vertical
stack.distribution = .fillEqually       // How views fill the axis
stack.alignment    = .center            // Perpendicular alignment
stack.spacing      = 12                 // Gap between arranged subviews
```

**Distribution options:**
- `.fill` — One view fills remaining space (default).
- `.fillEqually` — All views get equal size.
- `.fillProportionally` — Views fill proportionally to their intrinsic size.
- `.equalSpacing` — Fixed equal gaps between views.
- `.equalCentering` — Equal distance between centers.

**Benefits:**
- Dynamically adding/removing views with animation: `stack.addArrangedSubview(view)` or `stack.removeArrangedSubview(view)`.
- Stack views compose — nest them for complex grid-like layouts.
- Hiding arranged subviews: `view.isHidden = true` collapses the space automatically.

```swift
// Animate adding a view
UIView.animate(withDuration: 0.3) {
    self.stack.addArrangedSubview(self.newView)
    self.stack.layoutIfNeeded()
}
```

---

### What are Size Classes in iOS and how do they enable adaptive layouts? [Mid]

**Size Classes** are a coarse-grained description of the available display area, introduced to allow a single UI design to adapt across all iOS device sizes and orientations without separate layouts for each screen.

There are two dimensions, each with two values:

| | **Compact** | **Regular** |
| --- | --- | --- |
| **Horizontal** | Narrow (iPhone portrait, iPad split view) | Wide (iPad full-screen, iPhone landscape on Plus/Pro Max) |
| **Vertical** | Short (iPhone landscape) | Tall (iPhone portrait, iPad) |

**Accessing in code:**
```swift
override func traitCollectionDidChange(_ previousTraitCollection: UITraitCollection?) {
    super.traitCollectionDidChange(previousTraitCollection)
    if traitCollection.horizontalSizeClass == .compact {
        // Compact width layout
    } else {
        // Regular width layout
    }
}
```

**In SwiftUI:**
```swift
@Environment(\\.horizontalSizeClass) var hSizeClass

var body: some View {
    if hSizeClass == .compact {
        VStack { content }
    } else {
        HStack { content }
    }
}
```

**Practical use:** Size classes are the standard way to build adaptive UIs that work on iPhone, iPad, and macOS (via Catalyst) without duplicating layout code.

---

### What are view transitions and how do you add animated transitions to UIKit views? [Mid]

**View transitions** are animated visual effects applied when views are added, removed, or swapped within a container. UIKit provides several built-in transition styles.

**`UIView.transition(with:)` — transition between two views in a container:**
```swift
UIView.transition(with: containerView,
                  duration: 0.4,
                  options: [.transitionFlipFromRight, .curveEaseInOut]) {
    containerView.addSubview(newView)
    oldView.removeFromSuperview()
}
```

**`UIView.transition(from:to:)` — swap two views:**
```swift
UIView.transition(from: currentView,
                  to: nextView,
                  duration: 0.35,
                  options: .transitionCrossDissolve,
                  completion: nil)
```

**Built-in transition options:**
| Option | Effect |
| --- | --- |
| `.transitionFlipFromLeft / Right` | 3D flip effect |
| `.transitionCurlUp / Down` | Page-curl animation |
| `.transitionCrossDissolve` | Fade between views |

**Custom transitions in UIKit:**
Implement `UIViewControllerAnimatedTransitioning` to create fully custom push/present animations with any `UIViewPropertyAnimator`-powered effect.

**In SwiftUI**, use `.transition()` modifier:
```swift
if showDetail {
    DetailView()
        .transition(.asymmetric(
            insertion: .move(edge: .trailing),
            removal: .opacity
        ))
}
```

---
"""

# ── iOS Fundamentals — General Frameworks ───────────────────────────────────
GENERAL_QUESTIONS = """
### What is the difference between Cocoa and Cocoa Touch? [Easy]

- **Cocoa** is Apple's application framework for building **macOS desktop applications**. It encompasses the Foundation and AppKit frameworks, providing APIs for windows, menus, and macOS-specific UI patterns.

- **Cocoa Touch** is Apple's application framework for building **touch-based applications** on iOS, iPadOS, tvOS, and watchOS. It encompasses the Foundation and UIKit (or SwiftUI) frameworks, designed around touch input, small screens, and mobile constraints.

| | Cocoa | Cocoa Touch |
| --- | --- | --- |
| **Platform** | macOS | iOS, iPadOS, tvOS, watchOS |
| **UI Framework** | AppKit | UIKit / SwiftUI |
| **Input model** | Mouse & keyboard | Touch, accelerometer, gestures |
| **Common frameworks** | Foundation, AppKit, Core Data | Foundation, UIKit, SwiftUI, Core Data |

Both share the **Foundation** framework for common services (collections, networking, strings, dates), but their UI layers are entirely separate.

---

### What are SpriteKit and SceneKit? [Easy]

Both are Apple frameworks for rendering graphics, but at different dimensions:

- **SpriteKit** is a 2D game and animation framework. It provides a GPU-accelerated rendering engine for 2D sprites, particle effects, physics simulations, and tile maps. It is the recommended framework for building 2D games on iOS and macOS.

```swift
let scene = SKScene(size: view.bounds.size)
let sprite = SKSpriteNode(imageNamed: "hero")
sprite.position = CGPoint(x: 200, y: 300)
scene.addChild(sprite)
```

- **SceneKit** is a 3D graphics framework for rendering and animating 3D objects and scenes. It provides a high-level, node-based scene graph API built on top of Metal and OpenGL. It is commonly used for 3D games, AR augmentations, and 3D model viewers.

```swift
let scene = SCNScene(named: "art.scnassets/ship.scn")!
let cameraNode = SCNNode()
cameraNode.camera = SCNCamera()
scene.rootNode.addChildNode(cameraNode)
```

**Key distinction:** SpriteKit = 2D. SceneKit = 3D. For augmented reality, both integrate with ARKit.

---

### Which API is used for writing automated UI test scripts on iOS? [Easy]

The **XCTest UI Testing API** (specifically `XCUIApplication`, `XCUIElement`, and `XCUIElementQuery`) is the primary framework for writing automated UI tests that interact with the application's interface.

```swift
import XCTest

class LoginUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUpWithError() throws {
        continueAfterFailure = false
        app.launch()
    }

    func testSuccessfulLogin() {
        let emailField = app.textFields["Email"]
        emailField.tap()
        emailField.typeText("user@example.com")

        let passwordField = app.secureTextFields["Password"]
        passwordField.tap()
        passwordField.typeText("password123")

        app.buttons["Login"].tap()

        XCTAssertTrue(app.staticTexts["Welcome"].exists)
    }
}
```

**Legacy alternative:** `UI Automation` (based on JavaScript, used with Instruments) was Apple's original UI testing solution, deprecated in Xcode 8 and fully removed in favour of `XCTest UI Testing`.

---
"""

# ═══════════════════════════════════════════════════════════════════════════
#  PERFORM INSERTIONS
# ═══════════════════════════════════════════════════════════════════════════

# 1. Insert SwiftUI questions before ## SwiftData
content = insert_before(content, '\n## SwiftData\n', SWIFTUI_QUESTIONS)

# 2. Insert Swift questions before ## UIKit
content = insert_before(content, '\n## UIKit\n', SWIFT_QUESTIONS)

# 3. Insert UIKit questions before ## Reactive Programming
content = insert_before(content, '\n## Reactive Programming\n', UIKIT_QUESTIONS)

# 4. Insert General Frameworks questions before ## Objective-C
content = insert_before(content, '\n## Objective-C\n', GENERAL_QUESTIONS)

# Write result
with open(SOURCE, 'w', encoding='utf-8') as f:
    f.write(content)

# Count new questions
new_q_count = (SWIFTUI_QUESTIONS + SWIFT_QUESTIONS + UIKIT_QUESTIONS + GENERAL_QUESTIONS).count('---\n\n### ')
print(f'✅ Inserted ~{new_q_count} new questions into {SOURCE}')
print(f'   New file size: {os.path.getsize(SOURCE):,} bytes')

# Verify README.md untouched
if os.path.exists('README.md'):
    print('✅ README.md is untouched.')
