# iOS Interview Questions — Definitive Study Guide

> A comprehensive, categorized, and deduplicated reference for senior iOS developer interview preparation.
> Each question is tagged with a difficulty level: **[Easy]**, **[Mid]**, or **[Expert]**.

---

## Table of Contents

- [iOS Fundamentals](#ios-fundamentals)
- [Objective-C](#objective-c)
- [Swift Fundamentals](#swift-fundamentals)
- [UIKit](#uikit)
- [Reactive Programming](#reactive-programming)
  - [RxSwift](#rxswift)
  - [Combine](#combine)
- [Design Patterns & Architecture](#design-patterns-architecture)
- [Core Data & Persistence](#core-data-persistence)
- [SwiftUI](#swiftui)
- [SwiftData](#swiftdata)
- [Third-Party Libraries & Dependency Management](#third-party-libraries-dependency-management)
- [General Computer Science, OS & Multithreading](#general-computer-science-os-multithreading)

---

## iOS Fundamentals

*Core iOS platform concepts: application lifecycle, provisioning, push notifications, and OS-level features.*

---

### What are some common debugging techniques in iOS? [Easy]

iOS offers a range of debugging tools, from basic logging to sophisticated profiling:

- **`print` / `NSLog`:** Output values to the console. `NSLog` also includes a timestamp and is available in Objective-C.
- **Breakpoints:** Pause execution at a specific line. Use the Debug Bar and Variables View in Xcode to inspect state. **Conditional breakpoints** and **action breakpoints** (e.g., log a message without pausing) are especially powerful.
- **LLDB Debugger:** Type `po <expression>` (print object) or `p <expression>` in the console to inspect values at runtime.
- **Instruments:** Apple's profiling tool for detecting memory leaks, CPU/GPU usage, energy consumption, and network activity.
- **Crash Logs / Xcode Organizer:** Analyze symbolicated crash reports from TestFlight or the App Store.
- **View Debugger:** Capture and inspect the 3D layer hierarchy of your UI at runtime in Xcode.
- **Address Sanitizer / Thread Sanitizer:** Detect memory corruption and data races at build time.

---

### What are the five iOS application lifecycle states and how does an app transition between them? [Mid]

iOS applications can exist in one of **five execution states**:

| State | Description |
| --- | --- |
| **Not Running** | The app has not been launched, or was terminated by the system. |
| **Inactive** | The app is in the foreground but not receiving events (e.g., a phone call is incoming, or it is transitioning between states). |
| **Active** | The app is in the foreground and actively receiving and handling user events. |
| **Background** | The app is not visible but is executing code (e.g., finishing a download or playing audio). |
| **Suspended** | The app is in memory but not executing code. The system may silently purge it if memory is needed. |

**Typical Launch Transition:**
> Not Running → Inactive → Active

**Typical Dismissal Transition:**
> Active → Background → Suspended

**Key delegate callbacks (UIKit):**
- `applicationDidBecomeActive(_:)` — Entering Active state.
- `applicationWillResignActive(_:)` — Leaving Active state.
- `applicationDidEnterBackground(_:)` — Entering Background state.
- `applicationWillEnterForeground(_:)` — Returning from Background.
- `applicationWillTerminate(_:)` — App is about to be terminated.

---

### What is Key-Value Observing (KVO) and how does it compare to NSNotificationCenter? [Mid]

* **Key-Value Observing (KVO)** allows a controller or class to observe when a property value changes. It adds observers for a specific *keypath* and is used to observe changes in a property of a single object.
* **NSNotificationCenter** adds observers for *notifications* and is used when multiple, decoupled objects need to be notified of an event.

---

### What is a memory leak? [Easy]

A **memory leak** commonly occurs when an object is allocated in such a way that when it is no longer in use or needed, it is not released. In iOS programming, you create certain objects with **weak references** in order to avoid a strong-to-strong relationship that creates a retain cycle and a memory leak.

---

### Spot the bug that occurs in the following code. [Mid]

Consider the following code snippet inside a View Controller:

```swift
class ViewController: UIViewController {
    @IBOutlet var alert: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
        let frame = CGRect(x: 100, y: 100, width: 100, height: 50)
        self.alert = UILabel(frame: frame)
        self.alert.text = "Please wait..."
        self.view.addSubview(self.alert)
    }
    
    func runWaitTask() {
        DispatchQueue.global(qos: .default).async {
            sleep(10)
            self.alert.text = "Waiting over"
        }
    }
}
```

**The Bug:**
All UI updates must be performed on the **main thread**. The code attempts to update `self.alert.text` from a global background queue, which can lead to unpredictable behavior or crashes.

**The Fix:**
Dispatch the UI update back to the main thread:

```swift
DispatchQueue.global(qos: .default).async {
    sleep(10)
    DispatchQueue.main.async {
        self.alert.text = "Waiting over"
    }
}
```

---

### What is the difference between a shallow copy and a deep copy? [Mid]

* **Shallow Copy**: Also known as an address copy or call-by-reference. It duplicates the structure but not the elements themselves. Both the original and the copy point to the same objects in memory, meaning changes made in one reflect in the other. For collections, a shallow copy duplicates the collection structure, but the elements are shared.
* **Deep Copy**: Similar to call-by-value. It duplicates everything, meaning any object pointed to by the source is copied, and the destination points to this new copy. Two completely separate objects are created in memory, which is less prone to race conditions and performs well in a multithreaded environment. Value types in Swift are copied deeply by default, while reference types require explicit deep copying.

---

### What is a retain count and what is a retain cycle? [Mid]

* **Retain Count**: Represents the number of strong references (owners) pointing to a particular object in memory. When the retain count reaches zero, the object is deallocated.
* **Retain Cycle**: Occurs when two or more objects hold strong references to each other, creating a cycle. Because their retain counts never reach zero, neither object can be deallocated, leading to a memory leak.

---

### What are the differences between Delegation, Notification Center, and Key-Value Observing (KVO)? [Mid]

These are all communication patterns used to pass data between objects:
* **Delegation:** A one-to-one communication pattern using protocols. It is tightly coupled (the sender knows the delegate's type via a protocol) and relies on explicit method calls.
* **Notification Center:** A one-to-many communication pattern. It acts as a centralized hub where objects broadcast notifications and other objects observe them. It is loosely coupled, as the sender and receiver do not need to know about each other.
* **Key-Value Observing (KVO):** A mechanism that allows an object to be notified directly when a specific property of another object changes. It is useful for observing state changes but requires Objective-C runtime integration in Swift (`@objc dynamic`).

---

### What constraints exist when trying to use Key-Value Observing (KVO) on a Swift property? [Mid]

Because KVO relies heavily on the Objective-C runtime, you must meet specific constraints to observe a property in Swift:
1. The class containing the property must inherit from `NSObject`.
2. The property itself must be marked with the `@objc` and `dynamic` modifiers to ensure it uses dynamic dispatch rather than Swift's static dispatch.

---

### What is the difference between a Framework and a Library in iOS? [Easy]

- **Library:** A collection of reusable code (functions, classes, utilities) that your application calls. You control the flow — your code calls into the library. Examples: a JSON parsing utility, a math library.
- **Framework:** A structured bundle that can include libraries, resources (images, nibs, localization files), and headers. Critically, a framework can **invert the control flow** — it calls your code at defined points (e.g., delegate callbacks, lifecycle hooks). UIKit and Foundation are frameworks.

**In short:** A library is something you call. A framework calls you (Inversion of Control).

---

### What is the purpose of Unit and UI Testing, and what are their benefits? [Mid]

**Unit Testing** and **UI Testing** are fundamental practices for ensuring code quality and reliability, often utilized in Test-Driven Development (TDD).
* **Unit Testing:** Involves isolating specific parts of the program (like individual functions, classes, or modules) and testing them independently to ensure they behave exactly as expected.
* **UI Testing:** Focuses on simulating user interactions with the application's interface to verify that the app responds correctly to user inputs and visually functions as designed.

**Benefits:**
* Ensures that code meets its design and requirements.
* Catches bugs early in the development cycle.
* Facilitates safer code refactoring (acting as a safety net against regressions).
* Serves as living documentation for how the code is supposed to work.

---

### What is mocking in the context of iOS unit testing? [Mid]

Mocking is a technique used in unit testing where you create a fake, controlled version of an object or dependency (a "mock").

By replacing real components (like network managers, databases, or complex services) with mocks, you can isolate the specific piece of code you are testing. This ensures that tests run quickly, behave deterministically, and are immune to external failures or side effects.

---

### Can you perform a UI test on a UIView element's color? [Easy]

No, because in UI testing, you do not have direct access to the properties of the UI components. UI tests interact with the application through the Accessibility API, which exposes elements as `XCUIElement`.

This API provides information about the element's frame, label, and state, but it does not expose visual properties like `backgroundColor` or `textColor`.

---

### What is the process and purpose of code signing for iOS apps? [Mid]

Code signing ensures that an application was created by a known source and has not been tampered with or modified since it was signed. It is a mandatory requirement for running apps on physical iOS devices and submitting them to the App Store.

* **Digital Identity**: During the build process, Xcode uses your digital identity (a public/private key pair and a certificate) to sign the application. The private key creates the signature, while the Apple-issued certificate contains the public key to identify the developer.
* **Security**: If the executable code is modified even slightly, the signature becomes invalid, preventing the app from running. However, resources like images or `.nib` files are not signed and do not invalidate the signature.
* **Re-signing**: Signatures can be removed and replaced. For example, Apple re-signs all applications before distributing them on the App Store.

---

### What are the different app states in the iOS lifecycle? [Easy]

An iOS application transitions through several distinct states managed by the operating system:

* **Non-running**: The app has not been launched or was terminated by the system.
* **Inactive**: The app is running in the foreground but is not receiving events. This typically happens during brief transitions, such as receiving a phone call, an SMS, or a system prompt.
* **Active**: The app is running in the foreground and actively receiving events.
* **Background**: The app is running in the background and executing code (e.g., downloading content, playing audio).
* **Suspended**: The app is in the background but is not executing code. The system keeps the app in memory, but it can be purged without warning to free up resources.

---

### What programming languages are primarily used for iOS development? [Easy]

The primary programming language used for modern iOS development is **Swift**. Introduced by Apple in 2014, it is fast, safe, and continuously evolving.

**Objective-C** is the legacy language of iOS. While its usage for new projects has declined significantly in favor of Swift, it is still widely used in older codebases and framework integrations.

---

### What is a bounding box in iOS layout and graphics? [Easy]

A bounding box is the smallest rectangular frame that completely encloses an object, shape, text character, or graphical element on the screen.

In iOS, this is often represented by a `CGRect` (defined by an origin point `x, y` and a size `width, height`). It specifies the position and dimensions of the element within its parent coordinate system, serving as a fundamental concept in Core Graphics and view layout.

---

### What kind of settings are stored in the Info.plist file? [Easy]

The `Info.plist` (Information Property List) file stores essential configuration data and metadata about the application that the system needs before the app is even launched.

Common settings stored in this file include:
* **App Metadata**: Bundle identifier, version numbers, and display name.
* **Permissions**: Privacy usage descriptions (e.g., Camera, Location, Microphone access).
* **Capabilities**: Background modes, supported device orientations, and launch screen configurations.

A plist file can be formatted in Text, Binary, or XML, and typically stores data types like strings, numbers, booleans, arrays, dictionaries, and raw data.

---

### What must you know about performing UIKit operations on threads? [Easy]

**UIKit is not thread-safe.** All UIKit operations — including view updates, layout changes, animations, and any modification of the view hierarchy — **must** be performed on the **main thread**.

Performing UI updates on a background thread leads to undefined behavior, including visual glitches, crashes, or silent failures.

```swift
URLSession.shared.dataTask(with: url) { data, _, _ in
    // ✅ This runs on a background thread — safe for data processing
    guard let data = data, let image = UIImage(data: data) else { return }

    DispatchQueue.main.async {
        // ✅ UI update dispatched to the main thread
        self.imageView.image = image
    }
}.resume()
```

With **async/await**, use `@MainActor` to enforce main-thread execution:
```swift
@MainActor
func updateImage(_ image: UIImage) {
    imageView.image = image
}
```

---

### What is the difference between an App ID and a Bundle ID? [Easy]

- **Bundle ID:** A string (in reverse-DNS format, e.g., `com.yourcompany.appname`) that **you define** in Xcode to uniquely identify your application. The operating system uses it to identify the app's executable, map its resources, and manage settings like entitlements. No two apps on a device can share the same Bundle ID.

- **App ID:** A two-part identifier used by Apple's developer portal. It consists of your **Team ID** (assigned by Apple) and the **Bundle ID** (or a wildcard pattern). App IDs are used to associate your app with backend services like Push Notifications, App Groups, iCloud, and Sign in with Apple.

**In short:** Bundle ID is set by you in Xcode; App ID is registered in the Apple Developer portal and links your Bundle ID to Apple's services.

---

### What is Deep Linking in iOS? [Mid]

**Deep linking** is a technique that routes a user directly to a specific piece of content or screen within an app, rather than just launching the app to its home screen.

**Two primary mechanisms in iOS:**

1. **URL Schemes (Custom URLs):** Register a custom URL scheme in `Info.plist` (e.g., `myapp://`). Any URL with that scheme will open your app. **Limitation:** If the app is not installed, the link fails silently.

2. **Universal Links:** Standard HTTPS URLs associated with your domain via an `apple-app-site-association` (AASA) file. If the app is installed, iOS opens the app directly; if not, the browser opens the webpage. **Preferred approach** — more secure and provides a fallback.

```swift
// Handling Universal Links in AppDelegate
func application(_ application: UIApplication,
                 continue userActivity: NSUserActivity,
                 restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void) -> Bool {
    guard userActivity.activityType == NSUserActivityTypeBrowsingWeb,
          let url = userActivity.webpageURL else { return false }
    Router.handle(url)
    return true
}
```

---

### What is the use of NotificationCenter? [Easy]

`NotificationCenter` is a framework feature in iOS and macOS used for broadcasting and receiving system or custom messages across different parts of an application. It allows disparate objects to communicate without tightly coupling them together. 

*(Note: While the OS has a UI-level "Notification Center" for user alerts, programmatically, `NotificationCenter` acts as an internal broadcast hub for app components.)*

---

### What are iBeacons in iOS? [Mid]

iBeacons are Apple's implementation of Bluetooth Low-Energy (BLE) wireless technology to provide location-based information and services. They allow iOS devices to receive contextual information when in close physical proximity to beacon hardware transmitters.

---

### What are the different smart groups in Xcode? [Easy]

Smart groups in Xcode help organize project files dynamically:

* **Simple Smart Group:** A basic organizational group that filters your project files by type, name, or path.
* **Simple Expression Smart Group:** Enables filtering using more complex logical expressions, such as `name contains 'ViewController' AND path contains 'Controllers'`.
* **Custom Smart Group:** Offers the highest level of flexibility, allowing you to create customized filters using advanced predicates.

---

### What APIs are available for battery-efficient location tracking in iOS? [Mid]

* **Significant-Change Location Service:** Highly power-efficient; it delivers updates only when the user's location changes significantly (e.g., transitioning between cell towers, often tracking movements up to 1km).
* **Region Monitoring (Geofencing):** Triggers enter or exit events when the device crosses a defined geographical boundary (typically a radius of 100 meters or more).
* **Visit Events:** Monitors and logs when a user arrives at or departs from frequently visited locations (like a home or office).

---

### What is the preferred method for caching data in memory? [Easy]

`NSCache` is vastly preferable to a standard `Dictionary` for in-memory caching. `NSCache` is specifically engineered to automatically purge items when the system experiences low memory pressure, doing so intelligently to retain as much relevant data as possible. Furthermore, `NSCache` is thread-safe, supports arbitrary keys and values, and allows customizable eviction behaviors via delegate methods, making it a robust solution.

---

### What is the difference between a delegate and a notification in iOS development? [Mid]

* A **Delegate** represents a one-to-one communication pattern. It allows an object to communicate directly with exactly one assigned delegate object via a defined protocol.
* A **Notification** represents a one-to-many communication pattern. Messages are broadcast via `NotificationCenter` to any number of registered observers simultaneously, without requiring the sender to know who is listening.

---

### When is an iOS application considered to be in the "Active" state? [Easy]

An application is truly "Active" when it is executing in the foreground and directly receiving user interactions and system events. *(Note: If an app is executing code in the background for a limited, system-allotted time before being suspended, it is officially in the "Background" state, not the Active state.)*

---

### Which state does an iOS app reach briefly before being suspended? [Easy]

The **Background** state. Almost all applications pass through the Background state to execute final cleanup code before the operating system formally puts them into the Suspended state.

---

### What techniques can you use to reduce the size of an iOS application? [Mid]

* **App Thinning:** A comprehensive suite of techniques to optimize installation size based on the user's specific device.
* **App Slicing:** A subset of App Thinning where the App Store delivers only the assets (like 2x vs 3x images) strictly required for the target device's architecture.
* **On-Demand Resources (ODR):** Hosting heavy, non-immediate assets (like later game levels) on Apple's servers to be downloaded only when the user needs them.
* **Asset Cleanup:** Routinely identifying and removing obsolete or unused images and files from the project bundle.
* **Bitcode:** Compiling an intermediate representation of the code so Apple can re-optimize the binary on their end. *(Note: Apple deprecated Bitcode in Xcode 14, but it remains historically relevant).*

---

### What is the difference between a synchronous and asynchronous URLSession request? [Easy]

* A **Synchronous** network request forcibly blocks the thread it is called on until the entire data transfer completes. Doing this on the main thread causes the UI to freeze entirely.
* An **Asynchronous** request dispatches the operation to a background thread, allowing the main thread to continue processing user interactions unhindered. A completion handler, delegate, or `async/await` continuation is notified once the download finishes.

---

### What is the most critical rule when updating the UI in a multithreaded iOS application, and how do you enforce it? [Easy]

You must **always update the UI on the main thread** (or main queue). Doing otherwise can lead to unpredicted behavior, UI glitches, or crashes. You can ensure this by using `DispatchQueue.main.async` or marking functions/classes with `@MainActor` in modern Swift concurrency.

---

### What does the `main()` function do in an iOS app, and what is `UIApplicationMain`? [Mid]

Every iOS app has a `main()` C function as its entry point (auto-generated by Xcode). Its sole job is to call `UIApplicationMain`, which bootstraps the entire UIKit runtime.

```objective-c
int main(int argc, char * argv[]) {
    @autoreleasepool {
        return UIApplicationMain(argc, argv, nil, NSStringFromClass([AppDelegate class]));
    }
}
```

**What `UIApplicationMain` does:**
1. Creates the **`UIApplication` singleton** — the central controller of the app.
2. Creates the **`AppDelegate`** instance and sets it as the application's delegate.
3. Loads the initial UI from the main Storyboard (or programmatically).
4. Starts the **main run loop**, which continuously listens for and dispatches events (touches, timers, notifications).

In Swift, the entry point is handled via the `@main` attribute on `AppDelegate` (which implicitly calls `UIApplicationMain`), so no explicit `main.swift` is needed in standard project templates.

---

### What are the APNS payload size limits for push notifications? [Easy]

Apple Push Notification Service (APNs) imposes payload size limits depending on the notification type:

| Notification Type | Max Payload Size |
| --- | --- |
| **Regular remote notifications** (HTTP/2 API) | **4 KB** (4,096 bytes) |
| **VoIP notifications** (PushKit) | **5 KB** (5,120 bytes) |
| **Legacy binary interface** | **2 KB** (2,048 bytes) — deprecated |

> **Tip:** If you need to deliver rich content (images, videos), send a compact payload and use a **Notification Service Extension** to download and attach the media before the notification is displayed.

---

### What are the three local notification triggers in iOS? [Easy]

Local notifications are scheduled using `UNUserNotificationCenter`. There are three trigger types:

1. **`UNTimeIntervalNotificationTrigger`:** Fires after a specified number of seconds.
```swift
let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 60, repeats: false)
```

2. **`UNCalendarNotificationTrigger`:** Fires at a specific date and time (using `DateComponents`).
```swift
var components = DateComponents()
components.hour = 9
components.minute = 0
let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: true)
```

3. **`UNLocationNotificationTrigger`:** Fires when the device enters or exits a geographic region (`CLRegion`).
```swift
let region = CLCircularRegion(center: coordinate, radius: 100, identifier: "office")
region.notifyOnEntry = true
let trigger = UNLocationNotificationTrigger(region: region, repeats: false)
```

---

### What are VoIP push notifications and how do they differ from regular push notifications? [Mid]

**VoIP push notifications** are a specialized type of push notification delivered via Apple's **PushKit** framework (`PKPushRegistry`), specifically designed for Voice over IP applications.

**Key advantages over regular APNs:**
- **App is relaunched** automatically if it is not running when the VoIP push arrives.
- **Delivered immediately** without system-level delay, for a real-time call experience.
- **Higher payload limit** (5 KB vs 4 KB).
- The device can **wake from suspension** specifically to handle the call.

**Requirements:**
- A dedicated **VoIP Push Certificate** from the Apple Developer Portal.
- `PushKit` integration with `PKPushRegistry` and the `PKPushRegistryDelegate`.
- All incoming call VoIP pushes **must** be reported to `CallKit` (required by Apple since iOS 13).

```swift
let registry = PKPushRegistry(queue: .main)
registry.delegate = self
registry.desiredPushTypes = [.voIP]
```

---

### What is TestFlight? [Easy]

TestFlight is an Apple product that makes it easy to invite users to test your iOS, watchOS, and tvOS apps before you release them into the App Store. You can invite up to 10,000 testers using just their email addresses.

---

### What is `NSXMLParserDelegate`? [Mid]

It is a protocol in the Foundation framework used to define the behavior of a delegate object that manages the parsing of XML documents using `XMLParser`.

---

### What are the major purposes of Frameworks in iOS development? [Easy]

Frameworks have three major purposes:

* **Code encapsulation**
* **Code modularity**
* **Code reuse**

---

### What is Continuous Integration (CI)? [Easy]

Continuous Integration (CI) is a development practice that requires developers to integrate code into a shared repository several times a day. Each check-in is then verified by an automated build, allowing teams to detect problems early. Common tools include Xcode Server, Jenkins, Travis CI, and Fastlane.

---

### What is `UNNotificationContent`? [Mid]

`UNNotificationContent` is a read-only object that stores the content data inside a scheduled or delivered local or remote notification.

---

### What are the different types of In-App Purchase products? [Mid]

There are four main types of In-App Purchases:

* **Consumable products:** Can be purchased more than once and are depleted as they are used (e.g., extra lives in a game).
* **Non-consumable products:** Purchased once and do not expire. Users can restore this functionality in the future if they reinstall the app (e.g., premium features).
* **Non-Renewing Subscription:** Used for a certain amount of time and certain content without automatically renewing.
* **Auto-Renewing Subscription:** Used for recurring, automatically renewing subscriptions (e.g., monthly service access).

---

### What is HealthKit? [Easy]

HealthKit is an iOS framework that stores health and fitness data in a central, secure location. It takes in data from multiple sources (like different devices and apps) and allows users to control access to their data to maintain privacy.

---

### What is Core ML? [Mid]

Core ML is an iOS framework that allows you to efficiently process and run machine learning models directly on the device. It is commonly used for tasks like face detection, image recognition, and natural language processing.

---

### What are `libssl_iOS` and `libcrypto_iOS`? [Expert]

These are static libraries that help with the secure on-device cryptographic verification of App Store receipt files for In-App Purchases.

---

### What are the benefits of using Xcode Server? [Easy]

Xcode Server automates the integration process. It automatically checks out a project from source control, builds the app, runs automated tests, and archives the app for distribution.

---

### What is the AVFoundation framework? [Mid]

AVFoundation allows developers to create, play, and edit audio and visual media on a detailed level with time-based data. It provides separate sets of APIs for advanced video and audio manipulation.

---

### What is the difference between `NSInteger`, `Int`, and `NSNumber`? [Mid]

- **`NSInteger`**: A type definition that describes an integer — but it is not equivalent to `int` on 64-bit platforms. It is defined as `int` when building a 32-bit app and as `long` for 64-bit apps. Most of the time you can replace `int` with `NSInteger`.
- **`Int`**: A primitive data type in Swift.
- **`NSNumber`**: Stores numeric types as objects and can convert them into different formats. It can also retrieve a string representation.

---

### What is the difference between `NSSet` and `NSArray`? [Easy]

- **`NSSet`**: Primarily accesses items by comparison. They are unordered, and no duplication is allowed.
- **`NSArray`**: Accesses items by index. They allow duplicate items and are ordered.

---

### What is the difference between `NSDictionary` and `NSMutableArray`? [Easy]

- **`NSDictionary`**: Unordered and stores objects as key-value pairs. Objects are accessed by addressing them with an arbitrary string key.
- **`NSMutableArray`**: An ordered collection similar to `NSArray`, but its content is dynamic (i.e., elements can be added, removed, or changed after creation).

---

### What are the differences between `NSNotificationCenter`, Local Notifications, and Push Notifications? [Mid]

- **Local Notification**: Represents notifications that an application can schedule for presentation to its users at specific dates and times. The OS delivers the notification. It appears as an alert if the app is in the background.
- **`NSNotificationCenter`**: Internal to the running app and doesn't require a server or special setup. It is used to notify custom class objects internally using `NSNotification` messages.
- **Push Notification**: Requires Certificates, Identifiers & Profiles in the Apple Developer portal. This requires a server and special setup. The message is sent from the remote server through APNs (Apple Push Notification service) to the device.

---

### What is the difference between a Static and a Dynamic Library? [Mid]

- **Static Library (`.a`)**: Allows an application to load code into its address space at *compile time*. Results in a larger app size on disk and slower build times. Code is directly linked into the binary, meaning updates to the library require recompiling the entire app.
- **Dynamic Library (`.dylib` / `.framework`)**: Loads code into the address space at *run time*. Results in smaller binaries and allows libraries to be updated independently without recompiling the executable. They can have their own initializers and cleanup tasks.

---

### What is the difference between LLVM and Clang? [Expert]

- **Clang**: The front end of the LLVM toolchain for the C language family (C, C++, Objective-C). It takes the source code, performs lexical analysis and parsing, and generates an abstract syntax tree (LLVM IR).
- **LLVM**: The broader compiler infrastructure. It takes the intermediate representation (IR) from Clang, optimizes it, and serves as the backend to generate machine code for the target architecture.

---

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

## Objective-C

*Objective-C language features, runtime, memory management patterns, and interoperability with Swift.*

---

### Why do you generally create a weak reference when using `self` in a block? [Mid]

Sometimes it is necessary to capture **`self`** in a block, such as when defining a callback block. However, since blocks maintain strong references to any captured objects including **`self`**, this may lead to a strong reference cycle and a **memory leak**.

Instead, capturing a weak reference to **`self`** is recommended in order to avoid this issue:

```objective-c
SomeBlock * __weak weakSelf = self;
```

---

### What is the difference between `@synthesize` and `@dynamic`? [Mid]

* **`@synthesize`** generates getter and setter methods for your property at compile time.
* **`@dynamic`** tells the compiler that the getter and setter methods are implemented not by the class itself but somewhere else (like the superclass, or will be provided at runtime). Uses for `@dynamic` include subclasses of `NSManagedObject` (Core Data) or when delegating the responsibility of implementing the accessors.

---

### What is the difference between `_` vs `self.` in Objective-C? [Easy]

You typically use either when accessing a property in Objective-C.

* When you use **`_`**, you're referencing the actual instance variable directly. You should generally avoid this.
* Instead, you should use **`self.`** to ensure that any getter or setter actions are honored.

In the case that you write your own setter method, using **`_`** would not call that setter method. Using **`self.`** on the property, however, would call the setter method you implemented.

---

### What are blocks in Objective-C? [Easy]

**Blocks** are a language-level feature of Objective-C (and C/C++). They are objects that allow you to create distinct segments of code that can be passed around to methods or functions as if they were values. This means that a block is capable of being added to collections such as `NSArray` or `NSDictionary`. Blocks are also able to take arguments and return values similar to methods and functions.

The syntax to define a block literal uses the caret symbol (`^`):

```objective-c
^{
  NSLog(@"This is an example of a block");
}
```

---

### What is the difference between a category and an extension in Objective-C? [Mid]

A **category** and an **extension** are similar in functionality as they can both add additional instance and class methods to a class.

* An **extension** can only do so if the source code for the class being extended is available at compile time. This means that classes such as `NSString` cannot be extended.
* A **category**, however, can be used to add additional methods to a class without needing the original source code (e.g., adding methods to the `NSString` class).

---

### What is the difference between `atomic` and `nonatomic` synthesized properties? [Mid]

Properties in Objective-C are set to **`atomic`** by default.

* **`atomic`** properties guarantee thread-safety for the accessor methods. They ensure that a value is fully set (by the setter) or fully retrieved (by the getter) even if called simultaneously from different threads.
* **`nonatomic`** properties are not thread-safe. They are faster but can cause race conditions. If a setter and getter are called simultaneously, the getter might retrieve an incomplete or nil value before the setter finishes assigning the new value.

---

### What is the difference between strong, retain, and copy property attributes? [Mid]

* **`retain` / `strong`:** `strong` in ARC is equivalent to `retain` in manual reference counting. It increases the object's reference count by one. When you retain an object, you share the exact same instance in memory with whoever passed it to you.
* **`copy`:** Makes a full duplicate of an object and returns it with a retain count of 1. When you copy an object, you own the copied instance, and it is entirely independent of the original. This is commonly used for mutable types (like `NSString` or `NSArray`) to prevent the underlying data from changing unexpectedly.

---

### What is Objective-C? [Easy]

Objective-C is an object-oriented programming language previously utilized as Apple's primary language for operating system development. It combines the syntax and flow control benefits of C with the object-oriented messaging capabilities of Smalltalk. It acts as a superset of C, maintaining C's primitive types while adding specific syntax for defining classes and methods.

---

### What are the important data types in Objective-C? [Easy]

Some of the most important data types in Objective-C include:

* `BOOL`: A boolean value (`YES` or `NO`).
* `NSInteger`: An integer that automatically adapts to 32-bit or 64-bit architectures.
* `NSUInteger`: An unsigned integer.
* `NSString`: An object type used to represent sequences of characters.

---

### What is a Selector in Objective-C? [Mid]

A **selector** (`SEL`) is an Objective-C type that represents the name of a method. It acts as a unique compile-time identifier for a method, used to look up and invoke methods at runtime via the Objective-C message-dispatch system.

```objective-c
// Defining a selector
SEL mySelector = @selector(doSomething);
SEL selectorWithArg = @selector(doSomethingWith:);

// Calling a method via selector
[myObject performSelector:@selector(doSomething)];
[myObject performSelector:@selector(setName:) withObject:@"Alice"];
```

**In Swift**, you use the `#selector` expression, which provides compile-time validation:
```swift
button.addTarget(self, action: #selector(handleTap), for: .touchUpInside)

@objc func handleTap() {
    print("Button tapped")
}
```

Selectors are only unique by **name**, not by class. Two classes can have a method with the same selector name. The compiler ensures uniqueness within a compilation unit.

---

### What is NSBundle and what is the main bundle? [Easy]

A **bundle** is a structured directory on disk that packages executable code and its associated resources (images, sounds, localization strings, storyboards, frameworks). The operating system presents bundles as single files to the user.

**Bundle types:**
- **Application bundle (`.app`):** Contains the app executable and all its resources.
- **Framework bundle (`.framework`):** Reusable code and headers.
- **Plug-in bundle (`.bundle`):** Dynamically loadable code.

**Main Bundle:**
`Bundle.main` (Swift) / `[NSBundle mainBundle]` (Objective-C) refers to the bundle of the **currently running application**. It is the most commonly used bundle for accessing app resources.

```swift
// Accessing a resource in the main bundle
if let path = Bundle.main.path(forResource: "config", ofType: "json") {
    let data = try? Data(contentsOf: URL(fileURLWithPath: path))
}

// Accessing from a specific bundle (e.g., a framework)
let frameworkBundle = Bundle(for: MyFrameworkClass.self)
```

---

### What is the `id` type in Objective-C? [Easy]

`id` is a generic object pointer type in Objective-C. It can point to an instance of **any** Objective-C class. It is the closest Objective-C equivalent to Swift's `Any` for reference types.

```objective-c
id someObject = [[NSString alloc] initWithString:@"Hello"];
id anotherObject = [[NSArray alloc] initWithObjects:@1, @2, nil];
```

**Key characteristics:**
- `id` is implicitly a pointer type (you do not write `id *`).
- Because the type is not known at compile time, the compiler cannot check method availability — errors only surface at **runtime**.
- `id` is the supertype of all Objective-C objects (except primitive C types).

**In Swift**, you interact with Objective-C APIs using `id` as either `Any` or `AnyObject` depending on context.

---

### What is Method Swizzling? [Expert]

**Method Swizzling** is a runtime technique in Objective-C (and Swift, for `@objc` methods) that **replaces the implementation** of one method with another at runtime. It is made possible by the Objective-C runtime's dynamic method dispatch — methods are looked up by selector at runtime via the method dispatch table.

```objective-c
#import <objc/runtime.h>

@implementation UIViewController (Swizzling)

+ (void)load {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        Class class = [self class];
        SEL original = @selector(viewWillAppear:);
        SEL swizzled = @selector(swizzled_viewWillAppear:);
        method_exchangeImplementations(
            class_getInstanceMethod(class, original),
            class_getInstanceMethod(class, swizzled)
        );
    });
}

- (void)swizzled_viewWillAppear:(BOOL)animated {
    [self swizzled_viewWillAppear:animated]; // Calls original implementation
    NSLog(@"viewWillAppear: %@", self);
}

@end
```

**Common use cases:**
- Adding analytics/logging to UIKit lifecycle methods without subclassing.
- Overriding default framework behavior (e.g., disabling screenshots).
- Monkey-patching third-party code.

**Risks & caveats:**
- If done incorrectly it can cause **infinite recursion** or undefined behavior.
- Swizzled code is **invisible** and hard to debug — use sparingly.
- Not possible for non-`@objc` Swift methods (which use static dispatch).

---

### How do you access a variable inside a block in Objective-C? [Mid]

By using the `__block` storage type modifier in Objective-C, which allows the block to mutate the original captured variable.

---

### What is fast enumeration in Objective-C? [Easy]

Several Cocoa classes, including the collection classes, adopt the `NSFastEnumeration` protocol. You use it to retrieve elements held by an instance using a syntax similar to that of a standard C `for` loop:

```objective-c
NSArray *anArray = // get an array;
for (id element in anArray) {
    /* code that acts on the element */
}
```

---

### What is the difference between the `+` and `-` notation in Objective-C methods? [Easy]

In Objective-C, **Instance methods** begin with a `-` (minus) sign, while **Class-level methods** (similar to static methods) begin with a `+` (plus) sign.

---

### What is the difference between a Category and a Protocol? [Easy]

*This comparison is typically for Objective-C, where we have the concept of categories. In Swift, we use protocols and extensions.*
- **Protocol**: Declares a set of methods that a class must implement. Methods can be marked as optional or required for the implementing class using `@optional` and `@required` keywords.
- **Category**: Adds methods to an existing class (e.g., `NSObject`), without modifying the class itself or requiring subclassing.

---

### What is the difference between a Category and Inheritance? [Mid]

- **Categories**: Allow expanding the API of existing classes without changing their type. They are used to add new methods, not properties. *(Note: We can add properties in categories through Associated Objects).*
- **Inheritance**: Expands the API but introduces a new type. Additionally, subclassing lets you add state and properties.

---

### What is the difference between `atomic` and `nonatomic` properties? [Mid]

- **Atomic**: The default behavior for properties in Objective-C. It ensures the present process is completed by the CPU before another process accesses the variable, making the getter/setter thread-safe. It is slower due to locking mechanisms.
- **Non-Atomic**: Faster for synthesized code but not thread-safe. It may result in unexpected behavior or crashes when two different threads access the same variable at the same time.

---

### What is the difference between `assign` and `weak`? [Mid]

- **`weak`**: Used when you only want a pointer to the object without retaining it (useful for avoiding retain cycles, e.g., delegates). It will automatically nil out the pointer when the object is released.
- **`assign`**: Used for primitives (like `int`, `float`, `BOOL`). It behaves exactly like `weak` except it *does not* nil out the object when released, potentially leaving dangling pointers if used on objects. `assign` and `unsafe_unretained` are identical in usage.

---

### What is the difference between `nil`, `Nil`, and `NSNull` in Objective-C? [Easy]

- **`nil`**: A literal null value for Objective-C objects (e.g., `id obj = nil;`).
- **`Nil`**: A literal null value for Objective-C classes (e.g., `Class cls = Nil;`).
- **`NSNull`**: A singleton object used to represent a null value in collection objects (like `NSArray` or `NSDictionary`), which do not allow `nil` values.

---

### What is the difference between KVC and KVO? [Mid]

- **KVC (Key-Value Coding)**: A mechanism by which an object's properties can be accessed or modified using string keys at runtime rather than calling setter/getter methods directly.
- **KVO (Key-Value Observing)**: Allows an object to observe changes to a property value on another object. Whenever the property changes value, the observer is automatically notified.

---

### What is the difference between ARC and AutoRelease? [Expert]

- **ARC (Automatic Reference Counting)**: Handles memory management (retaining and releasing objects) at compile time inside the scope of functions.
- **Autorelease**: Still used within ARC. Autorelease pools (`@autoreleasepool`) are used to defer the release of temporary objects until the pool is explicitly drained (typically at the end of the run loop).

---

## Swift Fundamentals

*The Swift programming language: syntax, type system, generics, protocols, closures, and language features.*

---

### What is a protocol? How do you define one in Swift? [Easy]

A **protocol** defines a blueprint of methods, properties, and other requirements that a conforming type must implement. Any class, struct, or enum can conform to a protocol. Protocols enable **polymorphism** without inheritance and are fundamental to Swift's protocol-oriented programming paradigm.

```swift
protocol Drawable {
    var color: String { get }
    func draw()
}

// Optional methods via protocol extensions
extension Drawable {
    func draw() {
        print("Drawing a \(color) shape.") // Default implementation
    }
}

struct Circle: Drawable {
    let color = "red"
    // draw() is inherited from the extension
}
```

In Objective-C, protocols support `@required` (default) and `@optional` method declarations:
```objective-c
@protocol MyDataSource
- (NSUInteger)numberOfRecords;
@optional
- (NSString *)titleForRecordAtIndex:(NSUInteger)index;
@end
```

Protocols are heavily used in UIKit as **delegate** and **dataSource** contracts (e.g., `UITableViewDataSource`, `UITableViewDelegate`).

---

### What is the difference between `public` and `open` in Swift? Why is it important to have both? [Mid]

Both **`public`** and **`open`** access levels allow entities to be used from any source file from their defining module, and also from a source file from another module that imports the defining module. However, there are key differences regarding inheritance and overriding:

* **`public`**: Classes declared as `public` can only be subclassed within the module they are defined in. Similarly, `public` class members can only be overridden by subclasses within that same module.
* **`open`**: The `open` access level removes these limitations. Classes declared as `open` can be subclassed outside of their defining module, and `open` class members can be overridden outside of their defining module.

It is important to have both because some classes of libraries and frameworks are not designed to be subclassed or have their methods overridden (e.g., certain methods of `NSManagedObject` in Core Data). Using `public` prevents unexpected behavior by restricting inheritance, while `open` explicitly allows it.

---

### What is the difference between `var` and `let`? [Easy]

* **`var`** declares a variable whose value can be changed after it is initialized.
* **`let`** denotes a constant whose value cannot be changed once it is set.

---

### What is the difference between a struct and a class? [Easy]

The main difference is that **structs** are **value types** (stored on the stack) while **classes** are **reference types** (stored on the heap).

Classes have additional capabilities that structs do not:
* **Inheritance** enables one class to inherit the characteristics of another.
* **Type casting** enables you to check and interpret the type of a class instance at runtime.
* **Deinitializers** enable an instance of a class to free up any resources it has assigned.
* **Reference counting** allows more than one reference to a class instance.

---

### What is the difference between implicit and explicit typing in Swift? [Easy]

When referring to something as implicit or explicit, it often refers to how a variable or object is declared.

```swift
var name: String = "onthecodepath" // explicit
var name = "onthecodepath"         // implicit
```

* In the **explicit** declaration, the type of the variable (`String`) explicitly follows the name of the variable.
* In the **implicit** declaration, the `String` type is not explicitly written. Instead, Swift uses **type inference** to determine that `name` is of type `String` based on the assigned value.

---

### What is the difference between `Self` and `self` in Swift? [Easy]

* **`Self`** (capital **S**): Refers to the type that conforms to a protocol or the type of the current class, struct, or enum (e.g., `String` or `Int`).
* **`self`** (lowercase **s**): Refers to the specific instance or value of that type within its own scope (e.g., `"hello"` or `556`).

---

### What is the difference between functions and methods? [Easy]

* **Functions**: Self-contained chunks of code that perform a specific task. They are defined globally or outside of a specific type's scope.
* **Methods**: Functions that are associated with a particular type. Classes, structures, and enumerations can define instance methods, which encapsulate specific tasks and functionality for working with an instance of that given type.

---

### What is the difference between class (type) methods and instance methods? [Easy]

* **Class (Type) Methods**: Methods called on the type itself. Defined using the `static` or `class` keyword. The `class` keyword allows subclasses to override the method, whereas `static` prevents overriding.

```swift
class SomeClass {
    static func someTypeMethod() {
        // Implementation
    }
}
SomeClass.someTypeMethod()
```

* **Instance Methods**: Functions that belong to instances of a particular class, structure, or enumeration. They are called on a specific instantiated object.

```swift
class SomeClass {
    func someMethod() {
        // Implementation
    }
}
let someClass = SomeClass()
someClass.someMethod()
```

---

### What is the difference between static dispatch and dynamic dispatch? [Mid]

* **Static Dispatch**: Also known as compile-time dispatch or direct dispatch. It is a highly optimized, direct call where the compiler knows exactly which function implementation to execute at compile time. Used in value types, final classes, and protocol extensions.

```swift
extension Movable {
    func crawl() {
        print("Default crawling")
    }
}
```

* **Dynamic Dispatch**: Also known as runtime dispatch or table dispatch. The system looks for the specific method implementation in a compiler-created dispatch table (called a witness table in Swift) at runtime. Commonly used for class inheritance and protocol requirements.

```swift
protocol Movable {
    func walk()
}
```

---

### What is the difference between a `static` variable and a `class` variable? [Easy]

Both the `static` and `class` keywords allow us to attach properties to a type itself rather than to instances of the type.

* **`static`**: The property becomes owned by the type and **cannot** be overridden by subclasses.
* **`class`**: The property belongs to the type but **can** be overridden by subclasses.

```swift
class Person {
    static var count: Int {
        return 250
    }
    
    class var averageAge: Double {
        return 30
    }
}

class Student: Person {
    // THIS ISN'T ALLOWED:
    // override static var count: Int { return 150 }
    
    // THIS IS ALLOWED:
    override class var averageAge: Double {
        return 19.5
    }
}
```

---

### What is the difference between `super` and `self`? [Easy]

* **`super`**: A reference to the superclass (parent class), used to call implementations of properties or methods from the inherited class.
* **`self`**: A reference to the current object (instance) of the class or struct within its own scope.

---

### What is the difference between value types and reference types in Swift? [Easy]

Types in Swift fall into one of two categories:
* **Value Types:** Each instance keeps a unique copy of its data. When assigned to a variable or passed to a function, the data is copied. These are usually defined as a `struct`, `enum`, or tuple.
* **Reference Types:** Instances share a single copy of the data. When assigned to a variable or passed to a function, a reference to the same memory location is used. These are usually defined as a `class`.

---

### Explain common Swift keywords such as @escaping, inout, weak, unowned, and lazy. [Mid]

* **`@escaping`:** Used to indicate that a closure passed as a function argument can outlive the function's scope (i.e., it can be stored and executed after the function returns).
* **`inout`:** Allows a function to modify its parameters and have those changes persist outside the function's scope.
* **`weak`:** Defines a weak reference to an object, meaning it does not increase the object's retain count. It is always declared as an optional variable and automatically becomes `nil` when the referenced object is deallocated, preventing retain cycles.
* **`unowned`:** Similar to `weak`, but assumes the referenced object will never be `nil` during its use. If accessed after the object is deallocated, it causes a runtime crash.
* **`lazy`:** A computed property that is only initialized the first time it is accessed. It saves the value and reuses it on subsequent calls, making it ideal for expensive operations.
* **`@discardableResult`:** Suppresses the compiler warning when the return value of a function is not used.
* **`dynamic`:** Tells the compiler to use Objective-C dynamic dispatch instead of static dispatch, often used for Key-Value Observing (KVO).

---

### What is the difference between Designated and Convenience initializers, and how does initializer inheritance work? [Mid]

* **Designated Initializers:** The primary initializers for a class. They must fully initialize all properties introduced by their class and call a designated initializer from their immediate superclass (delegating up).
* **Convenience Initializers:** Secondary, supporting initializers. They must call another initializer from the same class (delegating across) and ultimately call a designated initializer. They offer shortcuts to common initialization patterns.

**Automatic Initializer Inheritance:**
* **Rule 1:** If a subclass does not define any custom designated initializers, it automatically inherits all of its superclass's designated initializers.
* **Rule 2:** If a subclass implements all of its superclass's designated initializers (either by inheriting them or overriding them), it automatically inherits all of the superclass's convenience initializers.

---

### How is memory managed in iOS, and what is a retain cycle? [Mid]

* **Memory Management (ARC):** iOS handles memory management using **Automatic Reference Counting (ARC)**. When an object has a strong reference pointing to it, ARC increases its retain count by 1. When the retain count drops to 0, ARC automatically deallocates the object from memory. ARC handles this automatically, but it cannot prevent reference cycles.
* **Retain Cycle:** A memory leak condition that occurs when two or more objects hold strong references to each other. Because they retain each other, their ARC reference counts never drop to zero, making it impossible for the system to release them from memory.
* **Avoiding Retain Cycles:** You can break retain cycles by using `weak` or `unowned` references.

---

### What is the difference between a static function and a class function? [Easy]

Both are type methods, meaning they are called on the type itself rather than on an instance of the type.
* **`static func`:** Cannot be overridden by subclasses. It is used in both value types (structs and enums) and reference types (classes).
* **`class func`:** Can only be used within classes. It behaves similarly to a static method but allows subclasses to override the method's implementation.

---

### What are the different access modifiers in Swift? [Mid]

Swift provides several access levels to restrict access to code:
* **`open`:** The least restrictive. Allows access and subclassing/overriding outside the defining module.
* **`public`:** Allows access outside the module, but subclassing/overriding is restricted to the module where it is defined.
* **`internal`:** The default access level. Allows access anywhere within the defining module, but not outside.
* **`fileprivate`:** Restricts access to the same source file.
* **`private`:** The most restrictive. Restricts access to the enclosing declaration and its extensions within the same file.

---

### Why does a struct not have a deinitializer (deinit)? [Mid]

Structs are **value types** and are typically allocated on the stack, whereas classes are reference types allocated on the heap. Because structs are not managed by Automatic Reference Counting (ARC) and do not have reference counts, the system automatically destroys them the moment they go out of scope. Therefore, there is no need for a `deinit` method to handle complex teardown or release operations.

---

### What is an associated type in Swift? [Mid]

An `associatedtype` provides a placeholder name for a type that is used within a protocol. The actual type to use for that placeholder is not specified until the protocol is adopted. It is essentially Swift's way of introducing generics into protocols.

---

### What are higher-order functions in Swift? [Mid]

A **higher-order function** is a function that either takes one or more functions as arguments, returns a function as its result, or both. They are a cornerstone of functional programming in Swift and promote **concise, declarative, and composable** code.

| Function | Purpose | Returns |
| --- | --- | --- |
| **`map`** | Transforms each element | New collection of transformed values |
| **`filter`** | Selects elements matching a predicate | New collection of matching elements |
| **`reduce`** | Combines all elements into one value | Single value |
| **`compactMap`** | Transforms and removes `nil` results | New non-optional collection |
| **`flatMap`** | Transforms and flattens nested collections | Single flat collection |
| **`sorted`** | Sorts elements by a given comparator | New sorted collection |

**Examples:**

```swift
let numbers = [1, 2, 3, 4, 5, 6]

// map — square each element
let squared = numbers.map { $0 * $0 }           // [1, 4, 9, 16, 25, 36]

// filter — keep only even numbers
let evens = numbers.filter { $0 % 2 == 0 }      // [2, 4, 6]

// reduce — sum all elements
let sum = numbers.reduce(0, +)                   // 21

// compactMap — parse strings, drop failures
let strings = ["1", "two", "3"]
let parsed = strings.compactMap { Int($0) }      // [1, 3]

// flatMap — flatten nested arrays
let nested = [[1, 2], [3, 4], [5, 6]]
let flat = nested.flatMap { $0 }                 // [1, 2, 3, 4, 5, 6]
```

**Why use them?**
- **Reduce boilerplate** — eliminates verbose `for` loops.
- **Improve readability** — declarative intent is immediately clear.
- **Enable chaining** — multiple operations can be composed fluently: `numbers.filter { $0 > 2 }.map { $0 * 2 }`.

---

### What are the main features of Swift, and what are its advantages and disadvantages? [Mid]

Swift is a modern, fast, and safe programming language with several powerful features:

**Main Features:**
* **Generics**: Write flexible, reusable functions and types.
* **Optionals**: Safely handle the absence of a value.
* **Value and Reference Types**: Strong support for structs, enums (value types), and classes (reference types).
* **Static Typing**: Type checking occurs at compile time, reducing runtime errors.
* **Protocols**: Powerful protocol-oriented programming capabilities.
* **Safety and Readability**: Clean syntax that prevents common programming errors.
* **Multiplatform**: Supports iOS, macOS, Linux, and other platforms.

**Advantages:**
* **Strong Typing**: Catches errors at compile time and provides more runtime security.
* **Predictability**: Deterministic behavior with optionals and generics ensures safe code.
* **Maintainability**: Clear syntax makes code easier to read and refactor, which is ideal for large customer-facing applications.

**Disadvantages:**
* **Restrictiveness**: The strict type system can sometimes feel overly restrictive.
* **Lack of Dynamism**: Unlike Objective-C, Swift lacks dynamic metaprogramming capabilities, which can be limiting when building highly dynamic libraries or frameworks.

---

### What are the different pattern matching techniques available in Swift? [Mid]

Swift provides several powerful pattern matching techniques, primarily used in `switch` statements, `if case`, and `guard case` constructs:

* **Tuple Patterns**: Match values against the corresponding elements of a tuple.
* **Type-Casting Patterns**: Use `is` or `as` to match values based on their specific type.
* **Wildcard Patterns**: Use the underscore (`_`) to match and ignore values you don't care about.
* **Optional Patterns**: Match against optional values using `x?` as a shorthand for `.some(x)`.
* **Enumeration Case Patterns**: Match values against specific cases of an `enum`, often extracting associated values.
* **Expression Patterns**: Match values against expressions, typically using the `~=` operator (e.g., checking if a number falls within a range).

---

### When should you use strong, weak, and unowned references in Swift? [Mid]

Memory management in Swift relies on Automatic Reference Counting (ARC) for reference types (classes). Value types (structs and enums) are not managed by ARC.

* **Strong**: This is the default reference type. Use it when an object needs to guarantee that another object remains in memory for as long as it holds the reference. It is primarily used in parent-to-child relationships.
* **Weak**: Use it to avoid retain cycles, particularly when a child references its parent or in delegate relationships. A `weak` reference does not increment the retain count and must be an Optional variable, as ARC will automatically set it to `nil` when the object it points to is deallocated.
* **Unowned**: Use it when the referenced object has the same or a longer lifetime than the referencing object. Like `weak`, it does not increment the retain count, but it is non-optional. If you try to access an `unowned` reference after its object has been deallocated, the app will crash.

---

### What are conditional conformances in Swift? [Mid]

Conditional conformances allow a generic type to conform to a protocol only if its underlying generic parameters satisfy specific conditions.

For example, you can declare that an `Array` conforms to the `Equatable` protocol, but *only if* the elements it contains also conform to `Equatable`. This ensures type safety and allows you to use protocol methods only when it makes logical sense.

```swift
extension Array: Equatable where Element: Equatable {
    // Implementation
}
```

---

### What is the primary difference between an Array and a Set in Swift? [Easy]

The main differences between an Array and a Set are ordering and uniqueness:

* **Array**: An ordered collection of elements. Items can appear multiple times (duplicates are allowed), and they are accessed by their index.
* **Set**: An unordered collection of unique elements. Duplicates are automatically removed, and looking up elements is highly efficient (typically O(1) time complexity).

---

### What are Tuples in Swift and when should they be used? [Easy]

A Tuple is a lightweight, unnamed structure that groups multiple values into a single compound value. The values within a tuple can be of any type and do not have to be the same.

Tuples are extremely useful for returning multiple values from a function call without needing to create a dedicated custom struct or class. For example, a function can return a tuple containing both a status code and a message:

```swift
func getStatus() -> (code: Int, message: String) {
    return (200, "Success")
}
```

---

### What are raw strings in Swift and how are they created? [Easy]

Raw strings in Swift allow you to write strings exactly as you see them, without needing to escape special characters like backslashes (`\`) or double quotes (`"`).

They are created by placing a pound symbol (`#`) before the opening quotation mark and after the closing quotation mark.

```swift
let regularString = "He said, \"Hello, World!\""
let rawString = #"He said, "Hello, World!""#
```

Raw strings are particularly useful when writing regular expressions or multi-line JSON structures directly in code.

---

### What are circular references (strong reference cycles) in Swift? [Mid]

A **circular reference** (or strong reference cycle) occurs when two or more objects strongly refer to each other, creating a cycle.
* When objects hold strong references to each other, it means that each object has strong ownership of the other.
* Because their reference counts can never drop to zero, they can **never be deallocated** by Automatic Reference Counting (ARC).
* This strong reference cycle keeps the objects alive indefinitely, leading to **memory leaks**.

---

### What are Extensions in Swift, can they contain stored properties, and how do they compare to Objective-C Categories? [Mid]

**Extensions in Swift** add new functionality to an existing class, structure, enumeration, or protocol type.
* They can add **computed properties**, define **methods**, provide new **initializers**, define **subscripts**, and make existing types conform to **protocols**.
* **Stored Properties:** You **cannot** add stored properties to a type through an extension in Swift. Stored properties must be initialized when an instance is created, and extensions cannot provide their own designated initializers.
* **Comparison with Objective-C Categories:**
  * **Extensions (Swift)** are similar to Objective-C Categories but do not have names. They can extend types for which you do not have the original source code.
  * **Categories (Objective-C)** allow adding methods outside of the main interface file, useful for extending built-in classes or classes without source access.
  * **Extensions (Objective-C)**, also known as Class Extensions, must be implemented in the main interface file and are used to declare private methods and properties. They cannot be used for extending built-in classes.

---

### What is a Half-Open Range Operator in Swift? [Easy]

A **Half-Open Range Operator** (`x..<y`) specifies a range between values `x` and `y` where `y` is **not included**.
* The operator specifies a range that includes the first value but excludes the final value.
* It is specifically useful when you work with **zero-based lists** such as arrays, where it's convenient to count from `0` up to (but not including) the length of the list.

---

### What are reference types in Swift? [Easy]

A **reference type** contains the location in memory where the data lives.
* When a reference type (like a `class`) is passed to a function or assigned to a new variable, instead of creating a new copy of the object, it just creates **another reference** to that same object.
* The instance is **shared** among all the different references, meaning a modification through one reference will affect all other references pointing to that same instance.

---

### What are nested functions in Swift? [Easy]

In Swift, a **nested function** is a function defined within the body of another function.
* Nested functions are useful for **organizing code** and encapsulating functionality within a larger function scope.
* They help in abstracting complex logic and breaking down large functions into smaller, more manageable parts while keeping those helper functions hidden from the outside scope.

---

### What are the different types of numeric literals in Swift? [Easy]

Swift supports several types of numeric literals to represent values in different bases:
* **Decimal Literals:** Base 10 (no prefix).
* **Binary Literals:** Base 2 (prefix `0b`).
* **Octal Literals:** Base 8 (prefix `0o`).
* **Hexadecimal Literals:** Base 16 (prefix `0x`).

---

### What are the different types of control transfer statements in Swift, and how is the `break` statement used? [Easy]

**Control Transfer Statements** change the order of execution in your code by transferring control from one piece of code to another. Swift has five control transfer statements:
* **`continue`**
* **`break`**
* **`fallthrough`**
* **`return`**
* **`throw`**

The **`break`** statement is specifically utilized within a loop to **immediately terminate** its execution. Additionally, it is used to exit a `case` within a `switch` statement. When a program encounters a specific condition, the `break` statement interrupts the current control flow and terminates the execution of that specific loop or switch block.

---

### What is inheritance in Swift, and what are the roles of a superclass and subclass? [Easy]

**Inheritance** is a fundamental behavior that differentiates classes from other types in Swift. It is a process by which a class inherits properties, methods, or other features from another class. This allows for writing different implementations while maintaining the same behaviors by reusing existing code.
* **Superclass:** The existing class from which properties and methods are inherited.
* **Subclass:** The new class that inherits characteristics from the superclass. A subclass can be further modified with new characteristics or by overriding inherited ones.

---

### How do you write comments in Swift? [Easy]

Comments are non-executable text used to explain code. In Swift, you can write them in two ways:
* **Single-line comments:** Use double forward slashes (`//`). Everything after the slashes on that line is ignored by the compiler.
* **Multi-line comments:** Use a forward slash followed by an asterisk (`/*`) to start the comment, and an asterisk followed by a forward slash (`*/`) to end it. Swift also allows multi-line comments to be nested.

---

### What is Optional Chaining in Swift? [Easy]

**Optional Chaining** is a process of querying and calling properties, methods, and subscripts on an optional that might currently be `nil`.
* If the optional contains a value, the property, method, or subscript call **succeeds**.
* If the optional is `nil`, the property, method, or subscript call **fails gracefully** and returns `nil`.
* Multiple queries can be chained together, and the entire chain fails if any link in the chain is `nil`.

---

### How do `switch` statements work in Swift, and how do they differ from other languages? [Mid]

In Swift, a `switch` statement evaluates a value and compares it against several possible matching patterns to determine which block of code to execute.
* **No Implicit Fallthrough:** Unlike C and Objective-C, Swift's `switch` statements do **not** "fall through" by default to the next case. This makes them safer and less prone to errors. You must explicitly use the `fallthrough` keyword if you want this behavior.
* **Exhaustiveness:** They must be **exhaustive**, meaning every possible value of the type being considered must be matched by a case (often handled by adding a `default` case).
* **Advanced Features:** Swift supports advanced features like compound cases, value bindings, and `where` clauses for complex pattern matching within cases.

---

### What are Property Observers in Swift, and what is the difference between `willSet` and `didSet`? [Easy]

**Property Observers** respond to changes in a property's value. They are highly useful for performing additional logic when a property's value changes, such as updating the User Interface (UI) or triggering other dependent methods.
* **`willSet`**: Called just **before** the value is stored. It provides a default parameter named `newValue` containing the upcoming value.
* **`didSet`**: Called immediately **after** the new value is stored. It provides a default parameter named `oldValue` containing the previous value.

---

### What is the difference between `try`, `try?`, and `try!` in Swift? [Mid]

All three keywords are used to call functions that are marked as `throws`, but they differ in how they handle potential errors:

| Keyword | Behavior | When to use |
| --- | --- | --- |
| **`try`** | Must be placed inside a `do-catch` block. Errors are caught and handled explicitly. | When you need to inspect and handle specific error cases. |
| **`try?`** | Converts the result into an optional. Returns `nil` on failure, discarding the error. | When you don't care about the specific error and can proceed with `nil`. |
| **`try!`** | Force-unwraps the result. **Crashes** at runtime if an error is thrown. | Only when you have absolute certainty the call can never fail (rare). |

```swift
// try — explicit error handling
do {
    let data = try loadFile(named: "config.json")
} catch FileError.notFound {
    print("File not found")
} catch {
    print("Unexpected error: \(error)")
}

// try? — optional result
let data = try? loadFile(named: "config.json") // nil if it fails

// try! — crash on failure (use sparingly)
let data = try! loadFile(named: "config.json") // Fatal error if file missing
```

---

### What is a Dictionary in Swift? [Easy]

A Dictionary in Swift is an unordered collection of items stored in key-value pairs. It uses a unique "key" to reliably store and retrieve an associated "value."

**Syntax:**
```swift
var dictionaryName = [KeyType: ValueType]()
```

**Example:**
```swift
var examResult = ["Neha": "44", "Adil": "56", "Era": "84"]
print(examResult)

// Output: ["Neha": "44", "Adil": "56", "Era": "84"]
// Keys: "Neha", "Adil", "Era"
// Values: "44", "56", "84"
```

---

### What is a closure in Swift, how does it differ from a function, and what is a completion handler? [Mid]

A **closure** in Swift is a self-contained block of code that can be passed around as a reference and executed at a later time. Closures can capture and store references to variables from their surrounding context. A **function** is essentially a named closure that performs a specific, defined task.

**Closures vs. Functions:**
* Closures can be stored in variables or constants.
* They can capture external variables.
* They can be passed as arguments or returned from other functions.

**Example of a Function:**
```swift
func add(_ a: Int, _ b: Int) -> Int {
    return a + b
}
```

**Example of a Closure:**
```swift
let numbers = [1, 2, 3, 4, 5]
let squaredNumbers = numbers.map { $0 * $0 }
// The closure { $0 * $0 } is passed to the map method.
```

**Completion Handlers:**
Completion handlers are closures passed as parameters into other functions. They are primarily used in asynchronous tasks (like network requests or animations) to notify the system when an operation has finished its execution. It is a highly effective technique for implementing callbacks.

**Escaping vs. Non-Escaping Closures:**
* **Non-Escaping (Default):** Executed within the function and deallocated after execution (e.g., `map`, `filter`).
* **Escaping (`@escaping`):** Stored and executed later, potentially after the function exits (e.g., asynchronous operations, completion handlers).

---

### What is the difference between strong, weak, and unowned references in Swift? [Mid]

In Swift, references handle memory management via Automatic Reference Counting (ARC):

* **Strong:** The default reference type. It increases the object's reference count and ensures the object is kept in memory as long as the strong reference exists. You use strong references when you want to "own" the referenced object.
* **Weak:** Does not increase the object's reference count. It allows the object to be safely deallocated when no other strong references to it exist, effectively preventing retain cycles. Because the object can be deallocated at any time, a weak reference is always an Optional and becomes `nil` automatically when the object is destroyed. Frequent use cases include delegate properties and subviews.
* **Unowned:** Similar to weak, it does not increase the reference count. However, an unowned reference is non-optional and assumes the object it points to will always be valid. If you attempt to access an unowned reference after the object has been deallocated, it will trigger a runtime crash. Use it only when you are certain the referenced object will outlive the reference.

**Example of preventing a retain cycle with weak:**
```swift
class Parent {
    var child: Child?
}

class Child {
    weak var parent: Parent?
}

let parent = Parent()
let child = Child()
parent.child = child
child.parent = parent // Prevents retain cycle
```

---

### What is a `guard` statement in Swift and when should it be used? [Easy]

A `guard` statement is used to transfer program control out of a scope (exiting a function or loop early) if a specific condition is not met. It is primarily used at the beginning of a function to validate input parameters or safely unwrap optionals.

**Why use `guard`?**
* **Avoids Deep Nesting:** Keeps the "happy path" of your code unnested and readable.
* **Requires an `else` Block:** Ensures that failure cases are explicitly handled (e.g., via `return`, `throw`, or `break`).
* **Safely Unwraps Optionals:** Variables unwrapped using `guard let` remain available in the rest of the scope.

**Example:**
```swift
func divide(_ a: Int, by b: Int) -> Int? {
    guard b != 0 else {
        return nil
    }
    return a / b
}
```

---

### What are computed properties, and when should you use them over methods? [Mid]

Computed properties do not physically store a value in memory. Instead, they provide a getter (and optionally a setter) to calculate and return a value dynamically based on underlying logic or the state of other stored properties every time they are accessed. They must always be declared as `var`. A computed property with only a getter is called read-only.

**Computed Property vs. Method**
In Swift, we often need to encapsulate logic that returns a value. We have two options: Computed Properties or Methods.

* **Computed Properties:**
  * **No stored value** — it calculates a result each time it's accessed.
  * **Idempotent** — should return the same result when called multiple times with the same state.
  * **No Side Effects** — should not modify any external state.
  * **Execution Complexity** — `O(1)` (should be quick).
  * **Can Take Parameters?** — No.
  * **Use Case** — Returning a derived value.

* **Methods:**
  * Can **modify state** (`mutating` for struct).
  * Can have **side effects**.
  * Can take **parameters**.
  * **Use Case** — Performing an action or complex calculation.

*Example of Computed Property:*
```swift
struct Circle {
    var radius: Double
    var area: Double {
        return Double.pi * radius * radius
    }
}
```

*Example of Method:*
```swift
struct Counter {
    var count = 0
    mutating func increment() {
        count += 1
    }
}
```

---

### What is dynamic dispatch? [Expert]

Dynamic dispatch is the runtime mechanism that determines which specific implementation of a polymorphic method or function to invoke. It provides architectural flexibility by allowing subclasses to override methods inherited from a parent class, ensuring the correct subclass implementation is executed when called. In Swift, dynamic dispatch is used by classes for overridden methods, usually resolved via a virtual table (vtable) or Objective-C message passing (`objc_msgSend`).

---

### What is the difference between == and === in Swift? [Easy]

* **`==` (Equal To):** An operator used to evaluate whether the *values* contained within two variables are equivalent.
* **`===` (Identical To / Strict Equality):** An identity operator used explicitly for reference types (classes) to determine if two variables both point to the exact same physical instance in memory.

---

### When would you use a deinit block in Swift? [Mid]

You utilize `deinit` to perform manual memory cleanup operations immediately before a class instance is permanently deallocated. While Swift's ARC handles standard memory deallocation automatically, `deinit` is vital for releasing custom system resources, invalidating timers, closing file handles, or removing notification observers.

---

### Given the following Swift code, what is the value of `u`? [Easy]

```swift
var x1 = [10, 20, 30, 40, 50]
var x2 = [10, 20, 30, 40, 50, 65]
let u = 5
```
Based strictly on the provided code snippet, the value of `u` is definitively assigned as **`5`**.

---

### How do you swap the values of two variables in Swift without using a built-in swap function? [Easy]

You can use an `inout` parameter in a function with a temporary variable:
```swift
func swapNumbers(x: inout Int, y: inout Int) {
    let temp = x
    x = y
    y = temp
}

var num1 = 20
var num2 = 60
swapNumbers(x: &num1, y: &num2)
print(num1, num2) // Output: 60, 20
```
Alternatively, Swift allows tuple destructuring to swap variables inline:
```swift
(num1, num2) = (num2, num1)
```

---

### What are Swift's access control levels? [Mid]

Swift provides five levels of access control, from most to least restrictive:

| Level | Visibility |
| --- | --- |
| **`private`** | Only within the **enclosing declaration** and extensions of that declaration **in the same file**. |
| **`fileprivate`** | Anywhere within the **same source file**. |
| **`internal`** | Anywhere within the **same module** (app or framework target). This is the **default** level. |
| **`public`** | Accessible from **any module**, but **cannot be subclassed or overridden** outside the defining module. |
| **`open`** | Accessible from **any module** and **can be subclassed and overridden** outside the defining module. The most permissive level. |

```swift
open class Vehicle { }           // Can be subclassed anywhere (e.g., in another framework)
public class Engine { }          // Accessible anywhere, but not subclassable externally
internal class Transmission { }  // Default: accessible only within same module
fileprivate func helper() { }    // Only accessible in this file
private var secret = 42          // Only in this scope
```

**Key distinction — `open` vs `public`:** `open` is needed when you build a framework and want consumers to subclass or override your types. `public` prevents that.

---

### What is the difference between `map`, `flatMap`, `filter`, and `reduce`? [Mid]

These are the four core higher-order functions on Swift collections:

| Function | What it does | Returns |
| --- | --- | --- |
| **`map`** | Applies a transform closure to every element | `[TransformedType]` |
| **`flatMap`** | Applies a transform and **flattens** one level of nesting; also removes `nil` from optionals when used on sequences of optionals | `[TransformedType]` (flat) |
| **`filter`** | Keeps only elements for which a predicate returns `true` | `[Element]` (subset) |
| **`reduce`** | Combines all elements into a single accumulated value | `ResultType` |

```swift
let numbers = [1, 2, 3, 4, 5]

let doubled   = numbers.map { $0 * 2 }          // [2, 4, 6, 8, 10]
let evens     = numbers.filter { $0 % 2 == 0 }  // [2, 4]
let sum       = numbers.reduce(0, +)            // 15

let nested    = [[1, 2], [3, 4]]
let flat      = nested.flatMap { $0 }           // [1, 2, 3, 4]

let optionals: [String?] = ["a", nil, "b"]
let valid     = optionals.compactMap { $0 }     // ["a", "b"]  (use compactMap for nil removal)
```

> **Note:** `flatMap` on a sequence of optionals has been superseded by `compactMap` for nil-removing transforms since Swift 4.1. Use `compactMap` to remove `nil`, and `flatMap` to flatten nested collections.

---

### What is a `typealias` in Swift? [Easy]

`typealias` introduces a named alias for any existing type, improving code readability and reducing verbosity.

```swift
typealias UserID     = Int
typealias Completion = (Result<Data, Error>) -> Void
typealias JSONDict   = [String: Any]

func fetchUser(id: UserID, completion: Completion) { ... }
```

Type aliases do not create new types — they are purely a naming convenience. The compiler treats `UserID` exactly the same as `Int`.

---

### What is type safety and type inference in Swift? [Easy]

- **Type Safety:** Swift is a strongly-typed language. Every variable has a fixed type, and you cannot pass a value of the wrong type to a function or assign it to an incompatible variable. The compiler catches type mismatches at **compile time**, preventing an entire class of runtime errors.

- **Type Inference:** You do not always need to explicitly declare a type. The compiler deduces the type from the initial value provided:

```swift
var name = "Alice"    // inferred as String
var count = 42        // inferred as Int
var pi = 3.14159      // inferred as Double
```

You can also use explicit **type annotations** when needed:
```swift
var score: Float = 9.5
let tuple: (Double, Double) = (3.14, 2.71)
```

---

### What are Optionals in Swift? Explain forced unwrapping, optional binding, and nil-coalescing. [Mid]

An **Optional** (`T?`) represents a value that may either contain a value of type `T` or be `nil`. Optionals are Swift's primary mechanism for expressing the absence of a value safely.

**Forced Unwrapping (`!`):**
Appending `!` asserts the optional is non-nil and extracts the value. If it is `nil`, the app crashes with a fatal error. Use sparingly.
```swift
let name: String? = "Alice"
print(name!)  // "Alice" — unsafe if name were nil
```

**Optional Binding (`if let` / `guard let`):**
Safely unwrap an optional by binding its value to a new constant only if it is non-nil.
```swift
if let name = name {
    print("Hello, \(name)")
}

guard let name = name else { return }  // Early exit if nil
print("Hello, \(name)")
```

**Nil-Coalescing Operator (`??`):**
Provides a default value if the optional is `nil`.
```swift
let displayName = name ?? "Guest"  // "Alice" if non-nil, else "Guest"
```

**Optional Chaining (`?`):**
Call methods or access properties on an optional; returns `nil` if any link in the chain is `nil`.
```swift
let count = user?.profile?.posts?.count  // nil if any optional is nil
```

---

### What is the `defer` keyword in Swift and when should you use it? [Mid]

`defer` schedules a block of code to execute immediately **before the current scope exits**, regardless of how the scope is exited (normal return, early return, error thrown, or break).

```swift
func processFile(named name: String) throws {
    let file = try openFile(named: name)
    defer { closeFile(file) }  // Guaranteed to run, no matter what

    guard file.isReadable else { return }  // Early return — defer still fires
    let data = try file.readData()
    process(data)
}  // closeFile() is called here
```

**Common use cases:**
- Releasing resources (closing files, releasing locks).
- Resetting state after a function completes.
- Balancing paired operations (lock/unlock, begin/commit).

Multiple `defer` blocks in the same scope execute in **reverse order** (LIFO — last in, first out).

---

### What are the benefits of `guard` in Swift? [Easy]

`guard` provides an **early exit** mechanism that improves readability by eliminating deeply nested `if-let` chains (the so-called "pyramid of doom").

**Without guard (pyramid of doom):**
```swift
func process(data: Data?) {
    if let data = data {
        if let json = try? JSONDecoder().decode(Model.self, from: data) {
            if json.isValid {
                // actual work — buried under 3 levels of nesting
            }
        }
    }
}
```

**With guard (flat, readable):**
```swift
func process(data: Data?) {
    guard let data = data else { return }
    guard let json = try? JSONDecoder().decode(Model.self, from: data) else { return }
    guard json.isValid else { return }
    // actual work — at the top level
}
```

**Key rules:**
- The `else` branch **must** exit scope (`return`, `throw`, `break`, `continue`, or `fatalError`).
- Bindings made in `guard let` are available **in the enclosing scope** after the guard, unlike `if let`.

---

### What are Generics in Swift and why are they useful? [Mid]

**Generics** allow you to write flexible, reusable functions and types that can work with **any type**, subject to optional constraints. They eliminate code duplication while maintaining type safety.

**Generic function:**
```swift
func swap<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

var x = 5, y = 10
swap(&x, &y) // Works for Int

var s1 = "hello", s2 = "world"
swap(&s1, &s2) // Works for String too
```

**Generic type:**
```swift
struct Stack<Element> {
    private var items: [Element] = []
    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element? { items.popLast() }
}
```

**Type Constraints:**
```swift
func findMax<T: Comparable>(_ array: [T]) -> T? {
    return array.max()
}
```

Generics are the foundation of Swift's standard library — `Array<Element>`, `Dictionary<Key, Value>`, `Optional<Wrapped>` are all generic types.

---

### What is an `inout` parameter and how does it differ from a regular parameter? [Mid]

In Swift, function parameters are **constants by default** — you cannot modify them inside the function body. An **`inout` parameter** passes the argument **by reference**, allowing the function to modify the caller's original variable.

```swift
func doubleInPlace(_ value: inout Int) {
    value *= 2
}

var number = 5
doubleInPlace(&number)  // & is required to pass by reference
print(number)           // 10 — original variable was modified
```

**Key differences:**

| | Regular Parameter | `inout` Parameter |
| --- | --- | --- |
| **Passed by** | Value (copy) | Reference |
| **Modifies caller's variable** | ❌ No | ✅ Yes |
| **Call-site syntax** | `func(x)` | `func(&x)` |
| **Can be constant?** | Yes | ❌ No — must be a `var` |

> **Note:** `inout` parameters cannot have default values and cannot be variadic. Operator overloads like `+=` use `inout` internally.

---

### What are stored, computed, and type properties in Swift? [Mid]

**Stored Properties:**
Store a constant or variable value directly in an instance. Available in classes and structs.
```swift
struct Point {
    var x: Double  // variable stored property
    let y: Double  // constant stored property
}
```

**Computed Properties:**
Do not store a value; instead, they calculate and return a value on demand. They always use `var`.
```swift
struct Circle {
    var radius: Double
    var area: Double {  // computed property
        return .pi * radius * radius
    }
    var diameter: Double {  // computed property with getter and setter
        get { return radius * 2 }
        set { radius = newValue / 2 }
    }
}
```

**Type Properties (`static` / `class`):**
Belong to the type itself, not to any instance. All instances share one copy.
```swift
struct Config {
    static let maxConnections = 10  // type property
}
print(Config.maxConnections)  // accessed on the type, not an instance
```

- Use `static` for both structs and classes (cannot be overridden).
- Use `class` for class type properties to allow subclasses to override them.

---

### What is initialization in Swift and what types of initializers exist? [Mid]

**Initialization** is the process of setting up a new instance of a type, ensuring all stored properties have valid initial values before the instance is used.

**Default Initializer:**
If all properties have defaults and no custom initializers are defined, Swift provides a free `init()` for structs and classes.

**Memberwise Initializer (Structs only):**
Structs automatically receive an initializer with parameters for each stored property:
```swift
struct Point { var x: Double; var y: Double }
let p = Point(x: 1.0, y: 2.0)  // free memberwise init
```

**Designated Initializer:**
The primary initializer. Must fully initialize all properties of the class and call a superclass designated initializer (if applicable).

**Convenience Initializer:**
A secondary, supporting initializer. Must call another initializer on the same class (`self.init(...)`) ultimately leading to a designated initializer.
```swift
class Vehicle {
    var seats: Int
    init(seats: Int) { self.seats = seats }  // designated
    convenience init() { self.init(seats: 4) }  // convenience
}
```

**Failable Initializer (`init?`):**
Returns `nil` if initialization fails based on invalid parameters.
```swift
struct Temperature {
    let celsius: Double
    init?(celsius: Double) {
        guard celsius >= -273.15 else { return nil }  // absolute zero
        self.celsius = celsius
    }
}
```

**Initializer Delegation:**
Value types (structs) can call other initializers in the same type using `self.init(...)` to avoid duplicating initialization code.

---

### What is the difference between `Any` and `AnyObject` in Swift? [Easy]

- **`Any`**: Represents an instance of any type at all, including function types, optional types, structs, enums, and classes. When a variable or constant is declared as type `Any`, it can hold any value of any type.
- **`AnyObject`**: Represents an instance of any class type, or any value derived from a class. It cannot represent structs, enums, or other non-class types. `AnyObject` is a reference type.

---

### What is the difference between function overloading and function overriding? [Easy]

- **Function Overloading:** A way to define multiple functions with the same name in a class or a module, but with different parameters. Overloading allows a function to behave differently based on the number, type, and order of its parameters. The compiler determines which version of the function to call based on the arguments passed in at compile time.
- **Function Overriding:** A way to provide a new implementation of a method that is already defined in a parent class or an interface. Overriding allows a subclass to provide its own implementation of a method inherited from its superclass. The version of the method called depends on the type of the object at runtime.

---

### What is the difference between a class name and a type name in Swift? [Mid]

- A **class name** refers specifically to a class, which is a blueprint for creating objects. A class defines properties, methods, and initializers that can be used to create instances of the class. A class is a reference type.
- A **type name** is a more general term that refers to any type in Swift, including classes, structs, enums, and protocols. A type defines a blueprint for creating values of a certain kind. Unlike a class, a type can be either a value type or a reference type.

---

### What is the difference between class, static, and instance methods and properties in Swift? [Mid]

- **Instance Methods/Properties:** Associated with an instance of a class, struct, or enumeration. Each instance has its own copy of the property, and instance methods provide ways to access and modify those properties. They can only be called on an instance.
- **Class Methods/Properties:** Associated with the type itself rather than an instance. They are indicated by the `class` keyword. Crucially, class methods and properties can be overridden by subclasses since they are dynamically dispatched. They can access other class-level properties but not instance-level ones.
- **Static Methods/Properties:** Also associated with the type itself and shared among all instances of the type. They are indicated by the `static` keyword. However, static methods and properties *cannot* be overridden by subclasses (essentially acting as `final class` methods). They cannot be used in polymorphism.

---

### What are the differences between a struct and a class in Swift? [Easy]

- **Inheritance:** Classes support inheritance, while structs do not.
- **Type:** Classes are reference types (passed by reference), while structs are value types (passed by value).
- **Initialization:** Classes require a defined initializer if properties don't have default values, whereas structs automatically provide a memberwise initializer by default.
- **Mutability:** When declaring a constant (`let`) of a struct type, the entire struct instance becomes immutable (properties cannot be changed even if marked as `var`). When declaring a constant (`let`) of a class type, the reference itself is immutable (cannot be reassigned), but the properties of the instance can still be modified.

---

### What is an escaping closure in Swift? [Mid]

A closure is said to **escape** a function when it is called after the function returns. Closures that may be called asynchronously — stored as a property, dispatched to another queue, or passed to a completion handler — must be marked with `@escaping`.

**Non-escaping (default):**
The closure is guaranteed to be executed before the function returns.
```swift
func doWork(task: () -> Void) {
    task() // Called synchronously — no @escaping needed
}
```

**Escaping:**
The closure outlives the function's scope — it is stored or dispatched for later.
```swift
var completionHandlers: [() -> Void] = []

func registerHandler(_ handler: @escaping () -> Void) {
    completionHandlers.append(handler) // Stored — must be @escaping
}

func fetchData(completion: @escaping (Data?) -> Void) {
    URLSession.shared.dataTask(with: url) { data, _, _ in
        completion(data) // Called after function returns — must be @escaping
    }.resume()
}
```

**Key implication:** Escaping closures can create **retain cycles**. When capturing `self` inside an escaping closure, always use `[weak self]` or `[unowned self]` as appropriate.

---

### What is a mutating function in Swift structs and enums? [Mid]

Structs and enums are **value types**. By default, the properties of a value type cannot be modified from within its own instance methods. The `mutating` keyword explicitly allows an instance method to **modify the instance's stored properties** (or even replace `self` entirely).

```swift
struct Counter {
    var count = 0

    mutating func increment() {
        count += 1  // This would be a compile error without 'mutating'
    }

    mutating func reset() {
        self = Counter()  // Can even replace self with a new instance
    }
}

var c = Counter()
c.increment()  // count = 1
c.reset()      // count = 0
```

**Key rules:**
- `mutating` is **only required for value types** (structs and enums). Classes do not need it.
- A `let` constant of a struct type **cannot** call mutating methods (because the instance is immutable).
- Protocol methods can be marked `mutating` to allow conforming value types to implement them with mutation.

---

### What is abstraction and how is it achieved in Swift? [Mid]

**Abstraction** is an OOP principle where you expose only the essential features of an entity while hiding implementation details. It allows you to define a contract (interface) without specifying how it is implemented.

Swift achieves abstraction through **protocols** and **protocol extensions**:

- A **protocol** defines the abstract interface (method and property requirements) — equivalent to an interface in Java or an abstract class in other languages.
- A **protocol extension** can provide **default implementations**, allowing partial abstraction (similar to abstract classes).

```swift
protocol Drawable {
    func draw()          // Abstract requirement
    var color: String { get }
}

extension Drawable {
    func draw() {        // Default implementation (protocol extension)
        print("Drawing a \(color) shape")
    }
}

struct Circle: Drawable {
    let color = "red"
    // draw() is inherited from the extension — can override if needed
}

struct Square: Drawable {
    let color = "blue"
    func draw() { print("Drawing a custom square") } // Custom override
}
```

**Key distinction from Objective-C:** Swift does not have `abstract` classes. The idiomatic Swift way is protocol + protocol extension.

---

### What are opaque return types (`some`) in Swift? [Expert]

**Opaque return types**, introduced in Swift 5.1, allow a function or property to return a value of a **specific concrete type** that conforms to a protocol, without revealing **which** concrete type it is. This is expressed using the `some` keyword.

```swift
protocol Shape { func area() -> Double }

struct Circle: Shape {
    var radius: Double
    func area() -> Double { .pi * radius * radius }
}

// Opaque return type — caller knows it's "some Shape", not that it's Circle
func makeShape() -> some Shape {
    return Circle(radius: 5)
}

let s = makeShape()
print(s.area()) // ✅ Works — but s's concrete type is opaque to the caller
```

**Why use `some` instead of a plain protocol type?**

| Feature | `some Shape` (Opaque) | `Shape` (Existential / Protocol) |
| --- | --- | --- |
| **Hides concrete type** | ✅ Yes | ❌ No |
| **Type safety** | ✅ Compile-time checked | ❌ Dynamic only |
| **Dispatch** | ✅ Static (faster) | ❌ Dynamic (slower) |
| **Can return multiple conforming types** | ❌ No (must always be same type) | ✅ Yes |
| **Supports `Self` / associated types** | ✅ Yes | ❌ No (existentials can't) |

**Key use case — SwiftUI:**
The `body` property of every SwiftUI view uses `some View`. This hides the complex, deeply nested generic view type while giving the compiler full type information for optimization.

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello")
    }
}
```

**When to use `some`:**
- When building APIs or libraries and you want to **hide implementation details**.
- When the function always returns the **same concrete type** but you don't want to expose it.
- When you need to use protocols with **associated types** as return values (existentials cannot do this).

---

### What is the difference between a struct and a class in Swift? [Mid]

This is one of the most fundamental distinctions in Swift. The core difference is **value semantics vs. reference semantics**.

| Feature | Struct | Class |
| --- | --- | --- |
| **Type** | **Value type** — copied when assigned or passed | **Reference type** — shared memory, multiple references |
| **Memory** | Allocated on the **stack** (typically faster) | Allocated on the **heap** (managed by ARC) |
| **Mutability** | Properties cannot be modified without `mutating` keyword | Properties can be modified freely |
| **Copying behavior** | Assignment creates an independent **copy** | Assignment creates another **reference** to the same instance |
| **Identity** | No identity. `==` compares values (requires `Equatable`) | Has identity. `===` checks if two references point to the same object |
| **Inheritance** | ❌ Not supported | ✅ Supported (single inheritance) |
| **`deinit`** | ❌ Not available | ✅ Available |
| **Thread safety** | ✅ Copies prevent data races | ❌ Shared state requires explicit synchronization |
| **ARC overhead** | ❌ None (no reference counting) | ✅ Yes — retain/release on every reference change |
| **Protocols** | ✅ Full conformance | ✅ Full conformance |

**Copying semantics (Copy-on-Write):**
```swift
var a = [1, 2, 3]  // Array is a struct
var b = a          // b gets a copy (logically — CoW defers actual copy)
b.append(4)
print(a)  // [1, 2, 3] — a is unchanged
print(b)  // [1, 2, 3, 4]
```

**Reference semantics:**
```swift
class Person { var name: String; init(_ n: String) { name = n } }
let p1 = Person("Alice")
let p2 = p1
p2.name = "Bob"
print(p1.name)  // "Bob" — p1 and p2 share the same instance
```

**When to use each:**
- **Prefer structs** for models, data containers, and anything that should be independent and thread-safe.
- **Use classes** when you need inheritance, identity semantics, Objective-C interoperability, or a shared mutable object graph.

> **Apple's guidance (WWDC):** Default to structs. Use classes only when you need reference semantics or class-specific features.

---

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
    print("Event: \(name), Tags: \(tags.joined(separator: ", "))")
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

## UIKit

*UIKit framework: view lifecycle, layout, table views, collection views, navigation, and UI components.*

---

### What key considerations apply when displaying remotely-downloaded images in a UITableView? [Mid]

Displaying remote images in a `UITableView` correctly requires handling asynchronous loading and cell reuse carefully:

1. **Download lazily:** Only begin downloading an image when the cell becomes visible (i.e., in `cellForRowAt indexPath:`).
2. **Download asynchronously:** Perform all network requests on a background thread (e.g., using `URLSession`) to keep the main thread free for scrolling.
3. **Handle cell reuse:** Cells are reused as the user scrolls. When an image finishes downloading, verify the cell at that index path is still displaying the same content before setting the image. Cancel stale requests if the cell is reused.
4. **Cache aggressively:** Use a memory cache (e.g., `NSCache`) to avoid re-downloading images already fetched during the session.
5. **Show a placeholder:** Display a placeholder image while the download is in progress to prevent visual gaps.
6. **Switch to main thread for UI updates:** Always update `UIImageView` on the main queue.

In production, third-party libraries such as **SDWebImage** or **Kingfisher** handle all of the above automatically.

---

### What is the difference between `viewDidLoad` and `viewDidAppear`, and which should you use to load data from a remote server? [Mid]

* **`viewDidLoad`** is called exactly once when the view hierarchy is first loaded into memory.
* **`viewDidAppear`** is called every time the view is presented to the user on the screen.

The choice strictly depends on the data's lifecycle requirements:
* Use **`viewDidLoad`** if the remote data is entirely static, highly cacheable, and only needs to be fetched exactly once.
* Use **`viewDidAppear`** if the data is highly dynamic or changes frequently, ensuring the content is always fresh whenever the user sees the view.

In both instances, network calls should be executed asynchronously on a background thread to avoid blocking the UI.

---

### What is the difference between `frame` and `bounds` of a `UIView`? [Easy]

A view object tracks its size and location using its `frame`, `bounds`, and `center` properties:

* **`frame`**: Specifies the size and location of the view in its **superview's** coordinate system.
* **`bounds`**: Specifies the size of the view (and its content origin) in the view's **own** local coordinate system. The `bounds.origin` is typically `(0, 0)`.
* **`center`**: Contains the known center point of the view in the **superview's** coordinate system.

---

### What is the purpose of the `reuseIdentifier`? [Easy]

The **`reuseIdentifier`** indicates that cells for a `UITableView` (or `UICollectionView`) can be reused. The view maintains an internal cache of cells with the appropriate identifier and allows them to be reused when `dequeueReusableCell(withIdentifier:)` is called. This significantly increases performance, as a new view does not have to be created from scratch for each cell that appears on the screen.

---

### What is Auto Layout and how does it work? [Easy]

**Auto Layout** dynamically calculates the size and position of all views in your view hierarchy based on constraints placed on those views. This constraint-based approach allows you to build user interfaces that dynamically respond to internal and external changes, such as screen rotations, different device sizes, or content size modifications.

---

### What is the difference between Auto Resizing Masks and Auto Layout? [Mid]

* **Auto Resizing Masks**: An older, simpler system that determines how a view resizes relative to its superview's bounds. It only defines spring and strut behaviors (flexible margins and width/height) and cannot handle complex relationships between sibling views.
* **Auto Layout**: A robust, constraint-based system that dynamically calculates the size and position of views based on mathematical relationships. It allows for complex layouts that adapt seamlessly to different screen sizes, orientations, and localization changes.

---

### What is the difference between Intrinsic Content Size and Fitting Size? [Mid]

* **Intrinsic Content Size**: Acts as an **input** to Auto Layout. It is the natural size a view requires to display its content (e.g., the size of a `UILabel` based on its text and font). When a view has an intrinsic content size, the system generates constraints to represent that size.
* **Fitting Size**: Acts as an **output** from the Auto Layout engine. It is the size calculated for a view based on its constraints. If the view lays out its subviews using Auto Layout, the system calculates a fitting size based on its content and relationships.

---

### What is the difference between content hugging priority and content compression resistance priority? [Mid]

* **Content Hugging Priority**: Defines how much a view resists being made **larger** than its intrinsic content size. A higher hugging priority means the view will strongly resist growing beyond its content size.
* **Content Compression Resistance Priority**: Defines how much a view resists being made **smaller** than its intrinsic content size. A higher compression resistance priority means the view will strongly resist shrinking below its intrinsic content size.

---

### What is the difference between `layoutIfNeeded()` and `setNeedsLayout()`? [Mid]

* **`layoutIfNeeded()`**: A **synchronous** operation. It forces the system to calculate the layout and redraw the view and its subviews immediately. Typically used within animation blocks to ensure layout updates are animated smoothly.
* **`setNeedsLayout()`**: An **asynchronous** operation. It simply invalidates the current layout and schedules a layout update for the next update cycle. The system will redraw the view and its subviews when it naturally processes the run loop.

---

### What is the difference between `UITableView` and `UICollectionView`? [Easy]

* **`UITableView`**: Displays data in a single-column, vertical list of rows. It is highly optimized for standard list layouts and provides built-in styles and standard accessories (like disclosure indicators or deletion controls).
* **`UICollectionView`**: A more flexible and customizable component. It can display items in grids, horizontal scrolls, custom layouts (using `UICollectionViewLayout`), and multiple columns. It easily handles complex arrangements compared to a table view, but it requires slightly more setup.

---

### What is the UIViewController lifecycle? [Mid]

The UIViewController lifecycle is the sequence of method calls made as a view controller's view is loaded, displayed, and eventually removed. Understanding it is essential for correctly placing initialization, layout, and teardown code.

```
init(coder:) / init(nibName:bundle:)
       ↓
  loadView()              ← Create the view hierarchy (override only if building UI programmatically)
       ↓
  viewDidLoad()           ← View is in memory. One-time setup: add subviews, configure data.
       ↓
  viewWillAppear(_:)      ← About to appear. Refresh data, start animations.
       ↓
  viewDidLayoutSubviews() ← Bounds are finalized. Safe for frame-dependent layout.
       ↓
  viewDidAppear(_:)       ← Fully visible. Start video/audio, begin tracking.
       ↓
  viewWillDisappear(_:)   ← About to leave screen. Save state, pause activity.
       ↓
  viewDidDisappear(_:)    ← Off screen. Stop sensors, cancel non-essential work.
       ↓
  deinit                  ← View controller deallocated.
```

**Key rules:**
- `viewDidLoad` is called **once**. `viewWillAppear` / `viewDidAppear` are called **every time** the view appears.
- Always call `super` in every overridden lifecycle method.
- Avoid heavy work in `viewDidLoad`; prefer lazy loading or background fetches.

---

### What is the difference between UIWindow and UIView? [Easy]

- **`UIView`** is the fundamental building block for all visual elements in UIKit. Every button, label, image, and custom control is a `UIView` subclass. Views draw content, handle touch events, and lay out their subviews.
- **`UIWindow`** is a special subclass of `UIView` that acts as the **root container** for your entire view hierarchy. It has no visual content of its own but provides the coordinate system and manages event dispatch to the correct view.

**Key differences:**

| | UIView | UIWindow |
| --- | --- | --- |
| **Purpose** | Displays content, handles touches | Root container, event routing |
| **Count per app** | Many (thousands possible) | Typically one (or a few for overlays) |
| **Visible content** | Yes | No (transparent container) |
| **Coordinate system** | Relative to superview | Absolute screen coordinates |

---

### What is `viewDidLayoutSubviews` and when is it called? [Mid]

`viewDidLayoutSubviews` is a lifecycle method in `UIViewController` that is called to notify the view controller that its view has just finished laying out its subviews. It is called every time the view's bounds change (e.g., device rotation, or when the view's frame is modified). This is the ideal place to make final adjustments to the UI, such as updating frames or calculating layout-dependent values, because the bounds and frames of the subviews are accurate at this point.

---

### What is Intrinsic Content Size, and how do Content Hugging and Compression Resistance priorities work? [Mid]

* **Intrinsic Content Size:** This is the natural size a view wants to be based on its content. For example, a `UILabel`'s intrinsic size is determined by its text and font, while a `UIImageView`'s size depends on the image it displays. Auto Layout uses this information to automatically create constraints for the view's width and height.
* **Content Hugging Priority (Content does not want to grow):** This priority dictates how strongly a view resists being stretched larger than its intrinsic content size. A higher hugging priority means the view will try to stay at its natural size and avoid expanding.
* **Content Compression Resistance Priority (Content does not want to shrink):** This priority defines how strongly a view resists being squished smaller than its intrinsic content size. A higher compression resistance priority ensures the view's content is not clipped or truncated.

---

### What is the difference between a NIB (XIB) file and a Storyboard? [Easy]

Both are used to visually design user interfaces in iOS, but they serve slightly different purposes:
* **NIB/XIB:** Used for designing a single view or a reusable component (e.g., custom `UITableViewCell` or a standalone view). It is better suited for modular, decoupled UI components and makes version control (merging conflicts) easier.
* **Storyboard:** Used to design the entire flow of an application. It contains multiple view controllers and defines the transitions (segues) between them. While it provides a great overview of the app's navigation, storyboards can become complex, slow to load, and prone to merge conflicts in larger teams.

---

### What are the different ways to navigate between view controllers in iOS? [Easy]

There are several ways to transition between view controllers in iOS:
* **UINavigationController:** Pushing and popping view controllers using a navigation stack (`pushViewController(_:animated:)` and `popViewController(animated:)`).
* **Modal Presentation:** Presenting a view controller modally over the current one (`present(_:animated:completion:)` and `dismiss(animated:completion:)`).
* **UITabBarController:** Switching between different view controllers using tabs at the bottom of the screen.
* **Segues (Storyboards):** Using visual transitions defined in Storyboards (e.g., Show, Present Modally, Custom).
* **Container View Controllers:** Embedding child view controllers within a parent view controller and transitioning between them programmatically.

---

### What is the difference between `plain` and `grouped` `UITableView` styles? [Easy]

* **Plain (`UITableView.Style.plain`):** Sections sit flush with each other. A key characteristic is that section headers and footers "float" or stick to the top/bottom of the screen as the user scrolls through the section's rows.
* **Grouped (`UITableView.Style.grouped`):** Sections are visually separated with default padding and a distinct background color. Section headers and footers scroll inline with the content and do not float at the top.

---

### What does the `clipsToBounds` property do? [Easy]

`clipsToBounds` is a boolean property on `UIView`.
* When set to **`true`**, any subviews that extend beyond the view's bounds will be clipped (hidden) at the view's edges.
* When set to **`false`** (the default), subviews will be completely visible even if they draw outside the parent view's frame. It is often used in combination with `layer.cornerRadius` to clip content to rounded corners.

---

### What is the purpose of `@IBDesignable` in iOS development? [Easy]

`@IBDesignable` is an attribute applied to custom `UIView` subclasses. It allows Interface Builder (Xcode's storyboard/xib editor) to render the custom view in real-time.

When combined with `@IBInspectable` properties (like corner radius, border width, or shadow color), developers can see how their custom layouts and visual effects will appear directly in the Interface Builder canvas without needing to build and run the app.

---

### What is the primary benefit of using child view controllers in iOS? [Mid]

One major benefit of using **child view controllers** is that it allows for better **modularization** and organization of code in an iOS app.
* By breaking down a large, complex view controller into smaller, more manageable child view controllers, it becomes easier to understand, test, and maintain the codebase.
* It promotes the **Single Responsibility Principle** by delegating distinct UI components or features to their own dedicated view controllers.

---

### What is the Responder Chain in iOS? [Mid]

The **Responder Chain** is a dynamic sequence of objects that receive the opportunity to respond to events.
* It represents the series of events that occur once we start interacting with an iOS application.
* Applications receive and handle events (like touches or motion) using **responder objects** (instances of `UIResponder`, such as `UIView`, `UIViewController`, and `UIApplication`).
* If a responder cannot handle an event, it passes the event up the chain to its next responder.

---

### How do you create a custom UIView in iOS? [Easy]

To create a custom `UIView`, you must create a subclass of `UIView` and implement the `draw(_:)` method to define its custom drawing behavior, or configure its subviews during initialization.

**Example using `draw(_:)`:**
```swift
class CustomView: UIView {
    override func draw(_ rect: CGRect) {
        guard let context = UIGraphicsGetCurrentContext() else { return }
        context.setFillColor(UIColor.red.cgColor)
        context.fill(rect)
    }
}
```

---

### How do you create a custom UITableViewCell in iOS? [Easy]

To create a custom table view cell, you define a new subclass of `UITableViewCell` and configure the necessary user interface elements within the cell's structure.

**Example:**
```swift
class CustomTableViewCell: UITableViewCell {
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var subtitleLabel: UILabel!
    @IBOutlet weak var customImageView: UIImageView!

    override func awakeFromNib() {
        super.awakeFromNib()
        // Customize the cell's initial appearance and behavior here
    }
}
```

---

### What is the purpose of the prepareForReuse() method in a UITableViewCell? [Easy]

The `prepareForReuse()` method is invoked on a reusable cell object immediately before it is returned by the table view to be populated with new data. It provides an opportunity to reset the cell's visual state—such as clearing out old text, removing legacy images, or canceling obsolete network requests—preventing visual artifacts when scrolling.

---

### Can you have multiple UIWindows in an iOS application? [Mid]

Yes. Multiple `UIWindow` instances can be used in scenarios like presenting custom alerts over the entire UI, displaying a secure screen cover when the app enters the background to avoid sensitive data in screenshots, or handling external displays.
There are default window levels defined, such as `.normal`, `.statusBar`, and `.alert`. To use an additional window, you create a new `UIWindow` instance, set its `windowLevel`, and call `makeKeyAndVisible()`.

---

### What are the primary drawbacks of using UITableView? [Easy]

The main drawback of `UITableView` is its restriction to a single-column, **vertical scrolling** layout. It lacks built-in support for complex grid layouts or horizontal scrolling, which are more easily achieved using `UICollectionView`.

---

### How do you handle the software keyboard obscuring important parts of the UI, such as text fields? [Mid]

This issue is typically resolved by embedding the UI content within a `UIScrollView`. You can observe keyboard notifications (such as `UIResponder.keyboardWillShowNotification` and `UIResponder.keyboardWillHideNotification`) using `NotificationCenter`. When these notifications are triggered, you adjust the `contentInset` and `scrollIndicatorInsets` of the scroll view to match the keyboard's height, ensuring the active text field remains visible.

---

### What are the three phases of Auto Layout's layout pass? [Mid]

Auto Layout processes the view hierarchy in three sequential passes before rendering:

1. **Constraint Update Pass (bottom-up):** The system traverses the view hierarchy from leaves to the root, calling `updateConstraints()` on each view that has been marked dirty. Override `updateConstraints()` to make constraint changes in response to view changes, but call `super` last.

2. **Layout Pass (top-down):** The system traverses from the root down, calling `layoutSubviews()` on each view. Here, frames are calculated based on the constraints resolved in pass 1. Override `layoutSubviews()` to manually adjust frame positioning after Auto Layout has done its work.

3. **Display Pass (top-down):** Views are redrawn by calling `draw(_:)`. The system only redraws views that are marked as needing display (via `setNeedsDisplay()`). This is where Core Graphics rendering happens.

> **Tip:** Call `setNeedsLayout()` to schedule a layout pass, `setNeedsUpdateConstraints()` to schedule a constraint update, and `setNeedsDisplay()` to schedule a redraw. Avoid calling these methods repeatedly in a tight loop.

---

### How do you make UITableView scrolling smooth and performant? [Expert]

Achieving smooth, 60fps (or 120fps on ProMotion) UITableView scrolling requires optimizing work in several layers:

**Cell Reuse:**
- Always dequeue cells with `dequeueReusableCell(withIdentifier:for:)` instead of creating new instances.
- Implement one cell type per data model type to keep dequeue logic simple.

**Avoid Heavy Work on the Main Thread:**
- Move image downloading and decoding to a background queue.
- Pre-process images (resize, apply corner radius) before assigning them — never apply `clipsToBounds` + `cornerRadius` live during scrolling.
- Use `willDisplay` delegate method to trigger background pre-fetching.

**Layout & Rendering:**
- Avoid transparent (`UIColor.clear`) backgrounds where possible; compositing transparent layers adds GPU overhead.
- Round all frame values to pixel boundaries (`floor`/`ceil` with `UIScreen.main.scale`) to prevent anti-aliasing.
- Use `CALayer`'s `shouldRasterize = true` for complex static cells (cache the rendered layer as a bitmap).
- Prefer fixed-height cells when possible; `UITableView.automaticDimension` is convenient but slower.

**Prefetching:**
- Adopt `UITableViewDataSourcePrefetching` to start loading data before cells are needed.

**Instruments:**
- Use the **Core Animation** instrument to identify dropped frames.
- Use **Time Profiler** to find expensive code on the main thread.

---

### What is the UIButton class hierarchy? [Easy]

```
NSObject
  └── UIResponder
        └── UIView
              └── UIControl
                    └── UIButton
```

- **`NSObject`:** Root class. Provides runtime introspection, KVO, and memory management hooks.
- **`UIResponder`:** Adds the ability to receive and handle touch, press, motion, and remote-control events via the responder chain.
- **`UIView`:** Provides drawing, layout, animation, and view hierarchy management.
- **`UIControl`:** Adds the **target-action** mechanism for user interaction events (e.g., `.touchUpInside`).
- **`UIButton`:** The concrete button with title, image, state management, and tap handling.

---

### What are UIResponder and UIControl and how do they relate? [Mid]

- **`UIResponder`** is the abstract base class that forms the backbone of UIKit's **event-handling system**. Any object that can respond to and handle events (touches, key presses, motion) inherits from `UIResponder`. Events travel along the **responder chain** — from the first responder upward through parent views and ultimately to the application object — until a responder handles them or they are discarded.

- **`UIControl`** is a subclass of `UIView` (which is a subclass of `UIResponder`) that implements the **target-action** pattern. Controls like `UIButton`, `UISlider`, and `UISwitch` inherit from `UIControl`. When a user interacts with a control, it sends action messages to registered targets.

```swift
button.addTarget(self, action: #selector(handleTap), for: .touchUpInside)
```

`UIControl` also manages **control state** (`normal`, `highlighted`, `disabled`, `selected`), which determines its appearance.

---

### What are the differences between Push, Modal, and Unwind segues? [Mid]

- **Push Segue:** Requires the source view controller to be embedded in a `UINavigationController`. The destination view controller is **pushed** onto the navigation stack, inheriting the navigation bar and gaining a back button. The transition slides horizontally.

- **Modal Segue (Present Modally):** The destination is presented **over** the current view controller. It does not inherit the navigation bar or back button. It typically animates up from the bottom. Use this for tasks that require user attention before returning (e.g., login, settings, form entry).

- **Unwind Segue:** Travels **backwards** through the view hierarchy, dismissing one or more view controllers to return to an earlier scene. You define an `@IBAction` method in the destination view controller and connect to it in the storyboard.

```swift
// Define in destination view controller
@IBAction func unwindToHome(_ segue: UIStoryboardSegue) {
    // Optionally read data from segue.source
}
```

---

### What is intrinsic content size and how does it affect Auto Layout? [Mid]

**Intrinsic content size** is the natural, content-driven size that a view requires to display its content without clipping or compression. Auto Layout uses intrinsic content size to infer missing constraints rather than requiring you to explicitly set width and height for every view.

**Common examples:**
- `UILabel` — height and width derived from font size and text length.
- `UIButton` — width and height from title and image padding.
- `UIImageView` — matches the image's pixel size.
- `UIView` — has no intrinsic content size by default (`CGSize(width: -1, height: -1)`).

**Content Hugging & Compression Resistance:**
- **Content Hugging Priority:** How strongly a view resists being stretched *larger* than its intrinsic size. (Higher = fights against growth)
- **Compression Resistance Priority:** How strongly a view resists being squeezed *smaller* than its intrinsic size. (Higher = fights against shrinking)

```swift
label.setContentHuggingPriority(.defaultHigh, for: .horizontal)
label.setContentCompressionResistancePriority(.required, for: .horizontal)
```

---

### What are CALayer objects and how do they relate to UIView? [Mid]

Every `UIView` has an underlying `CALayer` (Core Animation Layer) that is responsible for the **actual rendering** of the view's content to the screen. The relationship is:

- `UIView` handles **events, layout, and touch** — it is a high-level UIKit concept.
- `CALayer` handles **drawing, animation, and compositing** — it is a lower-level Core Animation concept.

**Why does this matter?**
- Properties like `cornerRadius`, `borderWidth`, `shadowOpacity`, `masksToBounds`, and `backgroundColor` are all `CALayer` properties.
- Animating `CALayer` properties directly (using `CABasicAnimation`) is more efficient than UIView-based animations for complex effects.
- You can add **custom sublayers** to a view's layer for effects like gradients (`CAGradientLayer`) or shapes (`CAShapeLayer`).

```swift
view.layer.cornerRadius = 12
view.layer.borderWidth = 1
view.layer.borderColor = UIColor.systemBlue.cgColor
view.clipsToBounds = true // clips subviews to layer boundary
```

---

### What are the key UIApplicationDelegate lifecycle methods and what do they do? [Mid]

The `UIApplicationDelegate` protocol defines methods called at critical points in the application's lifecycle:

| Method | When Called | Typical Use |
| --- | --- | --- |
| `application(_:willFinishLaunchingWithOptions:)` | Very start of launch | Restore state, register for notifications |
| `application(_:didFinishLaunchingWithOptions:)` | Launch nearly complete | Set up root view controller, initialize services |
| `applicationDidBecomeActive(_:)` | App enters foreground & becomes active | Restart timers, refresh UI |
| `applicationWillResignActive(_:)` | About to become inactive (e.g., call incoming) | Pause tasks, save state |
| `applicationDidEnterBackground(_:)` | App moved to background | Save data, release shared resources. You have ~5 seconds. |
| `applicationWillEnterForeground(_:)` | About to return to foreground | Undo background changes |
| `applicationWillTerminate(_:)` | App about to be terminated | Save final state |

> **Note:** In apps using `UIWindowSceneDelegate` (iOS 13+), scene-level lifecycle events (foreground/background transitions) are handled by `UIWindowSceneDelegate` methods instead of the app delegate.

---

### What is `accessibilityHint` in iOS? [Easy]

`accessibilityHint` describes the results of interacting with a user interface element. A hint should be supplied *only* if the result of an interaction is not obvious from the element’s standard label.

---

### Explain `CAEmitterLayer` and `CAEmitterCell`? [Mid]

UIKit (via Core Animation) provides these classes for creating particle effects.

* **`CAEmitterLayer`**: The layer that emits, animates, and renders the particle system.
* **`CAEmitterCell`**: Represents the source and defines the direction, velocity, and visual properties of the emitted particles.

---

### How is the app delegate declared by the Xcode project template? [Easy]

By default, the App Delegate is declared as a subclass of `UIResponder` and conforms to the `UIApplicationDelegate` protocol.

---

### What is the purpose of the `UIWindow` object? [Mid]

The presentation of one or more views on a screen is coordinated by the `UIWindow` object. It provides the basic container for an app's views and routes events to them.

---

### What is the lifecycle of a `UIViewController`? [Mid]

According to Apple's Documentation, the typical lifecycle methods include:

* **`loadView()`**: Subclasses should create their custom view hierarchy here if they aren’t using a storyboard/nib. Should never be called directly.
* **`loadViewIfNeeded()`**: Loads the view controller’s view if it has not already been set.
* **`viewDidLoad()`**: Called after the view has been loaded into memory.
* **`viewWillAppear(_:)`**: Called when the view is about to be made visible.
* **`viewWillLayoutSubviews()`**: Called just before the view controller’s view’s `layoutSubviews` method is invoked.
* **`viewDidLayoutSubviews()`**: Called when the size, position, and constraints have been applied to all objects.
* **`viewDidAppear(_:)`**: Called when the view has fully transitioned onto the screen.
* **`viewWillDisappear(_:)`**: Called when the view is about to be dismissed, covered, or hidden.
* **`viewDidDisappear(_:)`**: Called after the view was dismissed, covered, or hidden.
* **`viewWillTransition(to:with:)`**: Called when the view is transitioning or rotating.
* **`willMove(toParent:)`**: Called when transitioning between child controllers.
* **`didMove(toParent:)`**: Called after transitioning between child controllers.
* **`didReceiveMemoryWarning()`**: Called when the parent application receives a system memory warning.

---

### What is the difference between a XIB and a NIB? [Easy]

* **XIB (XML Interface Builder)**: These are flat XML files used for executable code in Xcode. They are editable but comparatively larger in size than a NIB.
* **NIB (NeXT Interface Builder)**: A non-editable, inoperable binary or archive file. After compilation, an Xcode XIB file is converted into a smaller, optimized NIB file.

---

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
@Environment(\.horizontalSizeClass) var hSizeClass

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

## Reactive Programming

*Reactive and declarative data-flow programming using RxSwift and Apple's Combine framework.*

---

### RxSwift

### What is Reactive Programming? [Mid]

Reactive programming is a declarative programming paradigm focused on dealing with asynchronous data streams and the propagation of change. It allows developers to safely observe and react to continuous streams of data (e.g., network responses, UI events like button taps or keyboard inputs) over time. In iOS, this is often implemented using frameworks like **RxSwift** or **Combine**.

---

### What are the primary components of RxSwift? [Easy]

The core building blocks of RxSwift are:
* **Observable:** The data producer. It represents a stream of data or events that can be observed over time.
* **Observer:** The consumer. It subscribes to an `Observable` and reacts to the items or events it emits.
* **DisposeBag:** A memory management tool used to automatically cancel subscriptions and release resources when the owning object is deallocated, preventing memory leaks and retain cycles.

---

### What are Observables, Subjects, and Drivers in RxSwift, and what are the different types of Subjects? [Expert]

* **Observable:** A data producer that emits events or notifications over time. Observers subscribe to it to react to these emissions.
* **Subject:** Acts as a bridge, functioning as both an **Observable** and an **Observer**. It can subscribe to other Observables and can also emit new elements to its own subscribers.
* **Driver:** A specialized `Observable` trait intended for the UI layer. It guarantees that events are delivered on the main thread, it never fails (cannot emit an error), and it shares side effects (multicasts).

**Types of Subjects:**
1. **PublishSubject:** Starts empty and only emits *new* elements to subscribers after they have subscribed. Previous events are not replayed.
2. **BehaviorSubject:** Requires an initial value. Upon subscription, it immediately replays its latest (or initial) value to the new subscriber, followed by any new elements.
3. **ReplaySubject:** Maintains a buffer of a specified size. When a new observer subscribes, it replays the entire buffer of previously emitted elements before emitting new ones.
4. **BehaviorRelay (formerly Variable):** A wrapper around a `BehaviorSubject` that stores its current value as state. It requires an initial value, replays the latest value upon subscription, and guarantees it will not terminate with an error.

---

### What is a `DisposeBag` and how does it work? [Mid]

A `DisposeBag` is an object used in RxSwift to manage memory and prevent retain cycles. In Rx, subscriptions to Observables return a `Disposable` object, which keeps the subscription active. By adding this `Disposable` to a `DisposeBag`, you tie the lifecycle of the subscription to the lifecycle of the object holding the `DisposeBag` (e.g., a `UIViewController`). When the owner of the `DisposeBag` is deallocated, the bag automatically calls `dispose()` on all its contents, safely releasing the subscriptions and freeing up memory.

---

### What is Reactive Programming in RxSwift and what key issues does it address? [Mid]

Reactive programming is used to handle mutable data processing and threads, such as fetching large amounts of data from an API. It addresses several key areas:

- **State:** Specifically, managing shared mutable state (the state of the data).
- **Imperative Programming:** Traditional programming uses functions to tell the app exactly *when* and *how* to do things, which can lead to complex state management.
- **Side Effects:** Issues arising during error handling or abnormal data processing (any change of state outside the current scope).
- **Declarative Code:** We specify functions that define pieces of behavior, and the framework executes this code. This eliminates issues related to side effects and state changes commonly found in imperative programming.
- **Reactive Systems:** Crucial for determining how the user interacts and how the response behaves. Reactive systems are:
  - **Responsive:** Always keep the UI up to date, representing the latest app state.
  - **Resilient:** Each behavior is defined in isolation, providing flexible error recovery.
  - **Elastic:** The code handles varied workloads, often implementing features such as lazy pull-driven data collections, event throttling, and resource sharing.
  - **Message-driven:** Components use message-based communication for improved reusability and isolation, decoupling the lifecycle and implementation of classes.

---

### What are the core building blocks of RxSwift, and how do they work? [Mid]

The three core building blocks of Rx code are **Observables**, **Operators**, and **Schedulers**.

- **Observables:** The generic class `Observable<T>` provides the foundation of Rx code by asynchronously producing a sequence of events. A sequence consists of data or events occurring asynchronously:
  - **Finite Observable Sequences:** Occur over a specific time (e.g., fetching data from an API).
  - **Infinite Observable Sequences:** Occur after an event interaction (e.g., a button tap triggering an observation every time it occurs).
  The `ObservableType` protocol allows one or more observers to react to any events in real-time. An Observable can emit only three types of events:
  - **`next` Event:** Carries the latest data value.
  - **`completed` Event:** Terminates the sequence with success, meaning the lifecycle completed successfully.
  - **`error` Event:** Terminates the sequence with an error.
- **Operators:** A set of methods used to apply Rx logic to the code. Operators like `filter`, `map`, and `subscribe` take an event as input, perform specific logic, and produce an output.
- **Schedulers:** RxSwift acts as a dispatcher between your subscriptions (the work being done) and the schedulers (the execution context). They send pieces of work to the correct context and seamlessly allow them to work with each other's output.

---

### Combine

## Design Patterns & Architecture

*Software architecture patterns (MVC, MVVM, VIPER), SOLID principles, and OOP design patterns.*

---

### What is the Singleton pattern? How do you implement a thread-safe Singleton in Swift? [Mid]

A **Singleton** is a creational design pattern that ensures **only one instance** of a class exists throughout the application's lifetime and provides a **global access point** to it. It is commonly used for shared services such as network managers, logging systems, or database managers.

**Basic Swift Singleton:**
```swift
class DatabaseManager {
    static let shared = DatabaseManager()
    private init() { } // Prevents external instantiation

    func fetchData() {
        print("Fetching data...")
    }
}
// Usage
DatabaseManager.shared.fetchData()
```
> `static let` in Swift is lazily initialized and thread-safe by default, so the basic pattern above is already safe.

**Thread-Safe Singleton for Mutable State:**
When the singleton holds mutable shared state (e.g., a cache dictionary), additional synchronization is needed:

*Approach 1 — Serial Queue (simple, serializes all access):*
```swift
class Logger {
    static let shared = Logger()
    private init() { }
    private let queue = DispatchQueue(label: "com.app.logger")
    private var log: [String] = []

    func append(_ entry: String) {
        queue.sync { log.append(entry) }
    }
}
```

*Approach 2 — Concurrent Queue with `.barrier` (optimized for read-heavy workloads):*
```swift
class Cache {
    static let shared = Cache()
    private init() { }
    private let queue = DispatchQueue(label: "com.app.cache", attributes: .concurrent)
    private var store: [String: Any] = [:]

    func write(key: String, value: Any) {
        queue.async(flags: .barrier) { self.store[key] = value } // Exclusive write
    }
    func read(key: String) -> Any? {
        return queue.sync { store[key] } // Concurrent reads
    }
}
```

| Feature | Serial Queue | Concurrent + Barrier |
| --- | --- | --- |
| **Read performance** | Serialized (slower) | Concurrent (faster) |
| **Write performance** | Serialized | Exclusive barrier |
| **Best for** | Low-traffic shared state | Read-heavy caches |

**Pros & Cons:**

| Pros ✅ | Cons ❌ |
| --- | --- |
| Single shared instance | Hard to unit test (global state) |
| Easy global access | Promotes tight coupling |
| Efficient resource management | Difficult to extend or subclass |

---

### What is the Delegation pattern? [Easy]

The **Delegation pattern** is a design pattern where one object (the *delegating object*) hands off certain responsibilities to another object (the *delegate*). The delegating object holds a reference to its delegate, typically as a **weak** reference to avoid retain cycles, and calls methods on it at the appropriate time.

**Key characteristics:**
- The relationship is **one-to-one** (one delegating object, one delegate).
- The contract between them is formalized using a **protocol**.
- It is used extensively in UIKit (e.g., `UITableViewDelegate`, `UITextFieldDelegate`).

```swift
protocol DataDownloaderDelegate: AnyObject {
    func didFinishDownloading(data: Data)
    func didFailWithError(_ error: Error)
}

class DataDownloader {
    weak var delegate: DataDownloaderDelegate?

    func startDownload() {
        // ... network call completes
        delegate?.didFinishDownloading(data: Data())
    }
}
```

---

### What is MVC and what is the 'Massive View Controller' problem? [Mid]

**MVC (Model-View-Controller)** is Apple's foundational software architecture pattern for iOS.

- **Model:** Manages data, business logic, and persistence.
- **View:** Renders the UI. Has no knowledge of the model.
- **Controller (UIViewController):** Acts as the mediator between Model and View — fetches data from the model and updates the view, and responds to user interactions.

**The Massive View Controller Problem:**
In practice, UIViewControllers often accumulate responsibilities they shouldn't own — networking, data transformation, navigation logic, and complex view management. This leads to bloated, hard-to-test files that may exceed thousands of lines. This anti-pattern is commonly nicknamed **"Massive View Controller"** (a tongue-in-cheek interpretation of the MVC acronym).

**Solutions:** Move responsibilities out of the view controller by adopting complementary patterns:
- **MVVM** — move presentation logic into a ViewModel.
- **Coordinator** — move navigation logic into a Coordinator.
- **VIPER / RIBs** — full separation into Interactor, Presenter, Router layers for large-scale apps.

---

### What is MVVM? [Mid]

**MVVM (Model-View-ViewModel)** is an architectural pattern that improves upon MVC by introducing a **ViewModel** layer that holds all presentation logic.

- **Model:** Raw data and business logic (same as MVC).
- **View / ViewController:** Passive UI layer. It binds to the ViewModel and renders whatever state it exposes.
- **ViewModel:** Transforms raw model data into view-ready values (e.g., formatting a `Date` into a display string). It has no reference to any UIKit type.

**Benefits over MVC:**
- ViewControllers become thin and focused solely on the UI.
- The ViewModel is easily unit-testable without any UI dependency.
- Works naturally with data-binding mechanisms like **Combine**, **RxSwift**, or `@Published` in SwiftUI.

```swift
class UserViewModel {
    private let user: User
    var displayName: String { return "\(user.firstName) \(user.lastName)" }
    var memberSince: String { return "Member since \(user.joinYear)" }
    init(user: User) { self.user = user }
}
```

---

### What is the difference between Composition, Aggregation, and Association? [Mid]

* **Association**: Implies a basic relationship between two objects where one uses the other (a "uses-a" relationship). For example, `Foo` uses `Bar`.
```swift
public class Foo {
    func baz(bar: Bar) {
        // Uses Bar
    }
}
```

* **Composition**: Implies strict ownership, where the parent object is entirely responsible for the lifetime of the child object (a "part-of" relationship). When `Foo` dies, `Bar` dies with it.
```swift
public class Foo {
    private let bar = Bar()
}
```

* **Aggregation**: A "has-a" relationship where the parent object borrows another object. The child object can exist independently. When `Foo` dies, `Bar` may live on.
```swift
public class Foo {
    private var bar: Bar
    
    init(bar: Bar) {
        self.bar = bar
    }
}
```

---

### What are the three main types of design patterns? [Easy]

1. **Creational**: Deal with object creation mechanisms, making a system independent of how its objects are created, composed, and represented. Examples: Singleton, Factory, Builder.
2. **Behavioral**: Deal with communication and assignment of responsibilities between objects. Examples: Observer, Delegate, Command.
3. **Structural**: Deal with object composition and defining relationships to form larger structures. Examples: Adapter, Facade, Decorator, Proxy.

---

### What is Dependency Injection, why do we use it, and what are the different ways to implement it? [Mid]

**Dependency Injection** is a design pattern where an object receives its dependencies from the outside rather than creating them itself. This contrasts with Dependency Inversion, which states that high-level modules should not depend on low-level modules, but rather both should depend on abstractions.

**Why use Dependency Injection?**
It provides abstraction, easier mocking, improved testability, readability, reusability, and less tight coupling.

**Three ways to implement Dependency Injection:**

1. **Initializer Injection**: Passing dependencies through the initializer.
```swift
final class ViewModel {
    private let userService: UserServiceProtocol 

    init(userService: UserServiceProtocol) { 
        self.userService = userService
    } 
}
```

2. **Property (Setter) Injection**: Exposing a property or method to inject the dependency after initialization.
```swift
final class ViewModel {
    private var userService: UserServiceProtocol? 

    func setUserService(userService: UserServiceProtocol) { 
        self.userService = userService
    }
}
```

3. **Interface (Method) Injection**: Providing dependencies through a specific method defined by a protocol.
```swift
protocol ServiceProtocol {
    func inject(userService: UserServiceProtocol)
}

final class ViewModel: ServiceProtocol {
    private var userService: UserServiceProtocol? 

    func inject(userService: UserServiceProtocol) { 
        self.userService = userService
    }
}
```

---

### When is the Facade design pattern mostly used? [Easy]

The **Facade** pattern is mostly used when interacting with complex **frameworks, repositories, or subsystems**. It provides a simplified, unified interface to a larger body of code, hiding the internal complexity from the client and making the API easier to consume.

---

### What are the downsides of using the Singleton design pattern? [Mid]

1. **Thread Safety**: Singletons are not inherently thread-safe. If initialization and access are not handled properly, you might end up with race conditions or multiple instances.
2. **Testing**: They introduce global state into an application, making unit testing very difficult as tests can unintentionally affect one another. It becomes challenging to run tests in isolation.
3. **Mocking**: It is hard to mock a Singleton because its dependencies are hidden inside the class rather than being explicitly injected.
4. **Hidden Dependencies**: Classes that use Singletons internally hide their dependencies, making the code harder to understand, track, and maintain.

---

### What is the difference between MVP and MVVM? [Mid]

**MVP (Model-View-Presenter):**
* Resolves the problem of having a dependent **View** by using a **Presenter** as a communication channel between the **Model** and **View**.
* A one-to-one relationship exists between the **Presenter** and the **View**.
* The **Presenter** has knowledge about the **View** (usually through a protocol).

**MVVM (Model-View-ViewModel):**
* This architectural pattern is more event-driven as it uses data binding, making it easier to separate core business logic from the **View**.
* Multiple **Views** can be mapped to a single **ViewModel**.
* The **ViewModel** has no reference to the **View**.

---

### What is the Delegation design pattern? [Easy]

Delegation is a one-to-one design pattern used to pass data or communicate between structs and classes. It allows one object to act on behalf of, or in coordination with, another object, typically by defining a protocol that encapsulates the delegated responsibilities.

---

### What is the difference between the Delegate pattern and Key-Value Observing (KVO)? [Mid]

Both the Delegate pattern and KVO establish communication between objects, but they serve different use cases:

* **Delegation**: Creates a one-to-one relationship. An object communicates back to its owner or another object using a clearly defined protocol. The delegate implements specific methods to respond to events.
* **Key-Value Observing (KVO)**: Creates a one-to-many relationship. An object broadcasts changes to a specific property. Any number of objects can observe this property and react when its value changes. Unlike delegation, KVO is not protocol-dependent and relies heavily on Objective-C runtime features.

---

### What are some design patterns commonly used in iOS development apart from MVC, Singleton, Observer, and Delegate? [Expert]

Beyond the standard Cocoa patterns, several other design patterns are frequently used in iOS development:

* **Factory Method**: Abstracts the initialization of objects, allowing subclasses or factory methods to determine the exact type of object to create at runtime. This hides complex `switch` or `if` statements.
* **Adapter**: Acts as a bridge between two incompatible interfaces. It wraps an existing class with a new interface, making it extremely useful when integrating third-party code without modifying the original source.
* **Decorator**: Dynamically adds functionality to an object at runtime by wrapping it. The decorator implements the same interface as the original object and forwards messages to it, optionally performing additional actions before or after.
* **Command**: Encapsulates a request or operation as an object. This allows you to parameterize clients with queues, requests, or operations, and provides support for undoable operations and delayed execution.
* **Template Method**: Defines the skeleton of an algorithm in a base class, allowing subclasses to override specific steps without changing the algorithm's structure. The abstract methods to be overridden are often called "hook" methods.

---

### What are the main object-oriented design principles? [Mid]

Good software design relies on both low-level and high-level principles to maintain scalable and readable code.

**High-Level Principles (SOLID):**
1. **Single Responsibility Principle**: A class should have only one reason to change.
2. **Open/Closed Principle**: Software entities should be open for extension but closed for modification.
3. **Liskov Substitution Principle**: Subtypes must be substitutable for their base types without altering program correctness.
4. **Interface Segregation Principle**: Clients should not be forced to depend on interfaces they do not use.
5. **Dependency Inversion Principle**: High-level modules should not depend on low-level modules; both should depend on abstractions.

**Low-Level Principles:**
1. **Tell, Don’t Ask**: Instruct an object to perform an action using its own data, rather than asking for its data to perform the action externally.
2. **Once and Only Once (DRY)**: Avoid code duplication by encapsulating repetitive logic in dedicated methods or components.
3. **Law of Demeter**: An object should only communicate with its immediate neighbors (e.g., avoid deep chaining like `a.getB().getC().doSomething()`).
4. **Favor Composition over Inheritance**: Composition allows for flexible behavior changes at runtime, whereas inheritance creates rigid, static hierarchies.
5. **Command Query Separation**: A method should either perform an action (Command) or return data (Query), but not both.

---

### What are design patterns and why are they used? [Easy]

Design patterns are proven, repeatable solutions to commonly occurring software engineering problems that arise during architectural design. They serve as templates to make code more robust, structured, scalable, and easier to maintain. By applying design patterns, developers express a conceptual solution rather than a strict implementation, resulting in software that is highly flexible and reusable.

Common design patterns include:

* **Facade**
* **Decorator**
* **Memento**
* **Adapter**

---

### How do you implement a singleton pattern in Swift? [Easy]

To implement a singleton pattern in Swift, you create a `static` instance property representing the shared instance, and explicitly mark the initializer as `private` to prevent other instances from being instantiated.

**Example:**
```swift
class MySingleton {
    static let shared = MySingleton()
    
    private init() { }
}
```

---

### What are some common Cocoa design patterns? [Mid]

Cocoa and Cocoa Touch frameworks heavily utilize several design patterns:

* **Creational - Singleton:** Ensures that a class has only one globally accessible instance. It is highly useful for sharing resources or configuration settings across an entire application (e.g., `UserDefaults.standard`).
* **Behavioral - Memento:** Allows an object's internal state to be captured, saved externally, and restored later without violating encapsulation. It is frequently used for Undo/Redo functionality.
* **Structural - Decorator:** Enables behaviors to be added to individual objects dynamically without altering the class structure. It is ideal for modifying object behavior at runtime, commonly seen in Swift extensions or wrappers.

---

### What is the Adapter design pattern? [Mid]

The Adapter pattern is a structural design pattern that acts as a bridge between two incompatible interfaces. It involves a single class that wraps an existing interface and translates it into an interface that clients expect. 

A real-world analogy is a hardware dongle that allows an Ethernet cable to connect to a USB port. In software, it allows objects with otherwise incompatible interfaces to collaborate seamlessly.

---

### What is the difference between Delegation and Notifications? [Mid]

- **Delegates**: Create a "has-a" relationship between two classes. It supports two-way communication (we can return a value and the delegate has a chance to modify or reject operations). It checks protocol method implementation at compile time. Only one designated object can listen to the message. It avoids tight coupling.
- **Notifications**: Based on one-to-many communication. They cannot receive feedback and have no direct link between the objects communicating back and forth. There is no compile-time checking for method implementation. Any number of objects can receive the message.

---

### What is the difference between Delegate and Target-Action? [Mid]

- **Delegates**: Implemented using Protocols. This is a formal way of communicating across classes and is useful when more than one method may be needed. It is used for two-way communication where methods can return values to the sender.
- **Target-Action**: Generally used to correspond to an "event-like" situation, such as a button click or a timer firing. It is more suitable when communication is limited to control events or state changes. It mostly manifests one-way communication.

---

### What are the SOLID principles? [Mid]

The SOLID principles are a set of five design principles intended to make software designs more understandable, flexible, and maintainable:
- **S**ingle Responsibility Principle: A class should have only one reason to change.
- **O**pen/Closed Principle: Software entities should be open for extension but closed for modification.
- **L**iskov Substitution Principle: Subtypes must be substitutable for their base types without altering the correctness of the program.
- **I**nterface Segregation Principle: Clients should not be forced to depend on interfaces they do not use.
- **D**ependency Inversion Principle: High-level modules should not depend on low-level modules; both should depend on abstractions.

---

### What is the Singleton design pattern and when should it be used? [Easy]

The Singleton is a creational design pattern that ensures a class has only one single shared instance throughout the application's lifecycle while providing a global point of access to it. It is typically used for managing shared resources like network managers, database connections, or user defaults.

*Note:* Singletons can make unit testing more difficult because they carry global state across tests, so they should be used judiciously.

---

## Core Data & Persistence

*Data persistence using Core Data, NSUserDefaults, Keychain, and other storage mechanisms.*

---

### What is Core Data and when should you use it over NSUserDefaults? [Mid]

**Core Data** is Apple's object graph management and persistence framework. It manages model-layer objects and can persist them to a backing store (SQLite, binary, or in-memory). Data is organized into a relational entity-attribute model.

**NSUserDefaults vs. Core Data:**

| Criterion | NSUserDefaults | Core Data |
| --- | --- | --- |
| **Best for** | Small, simple data (settings, preferences, flags) | Large, structured, or relational datasets |
| **Data volume** | Small key-value pairs | Potentially millions of objects |
| **Querying** | No query support | Full predicate-based fetch requests |
| **Relationships** | None | Supports one-to-many, many-to-many |
| **Overhead** | Minimal | Higher (stack setup required) |

**Use NSUserDefaults** when you need to persist user preferences, feature flags, or small scalar values.
**Use Core Data** when you need to persist a large collection of structured objects, require querying/filtering, or need undo/redo support.

---

### What is an NSManagedObjectContext? [Mid]

An `NSManagedObjectContext` (MOC) is the **central scratchpad** of the Core Data stack. It is an in-memory workspace where you create, fetch, modify, and delete managed objects before committing changes to the persistent store.

**Key responsibilities:**
- Creating and fetching `NSManagedObject` instances.
- Tracking changes and supporting **undo/redo** operations.
- Saving (committing) changes to the persistent store coordinator.

**Important notes:**
- You may have multiple MOCs (e.g., a main-queue context for UI and a private-queue context for background imports).
- Each persistent store record is represented by **at most one** managed object per context.
- MOCs are **not thread-safe** — always use a context on the queue it was created for (main queue or private queue).

---

### What is NSFetchRequest? [Easy]

`NSFetchRequest` is the class responsible for fetching managed objects from Core Data. It encapsulates the query criteria and can be used to:

- Fetch a **set of objects** matching a given `NSPredicate`.
- Sort results using `NSSortDescriptor` objects.
- Limit results with `fetchLimit` and `fetchOffset`.
- Fetch **individual property values** (dictionaries) rather than full objects for efficiency.

```swift
let request = NSFetchRequest<Employee>(entityName: "Employee")
request.predicate = NSPredicate(format: "salary > %d", 50000)
request.sortDescriptors = [NSSortDescriptor(key: "lastName", ascending: true)]
let results = try context.fetch(request)
```

---

### Is Core Data thread-safe? [Mid]

No, Core Data is not thread-safe. `NSManagedObject` and `NSManagedObjectContext` instances must only be accessed on the thread where they were created. To safely use Core Data across multiple threads, you should use the `perform(_:)` or `performAndWait(_:)` blocks provided by `NSManagedObjectContext`, which guarantee that operations are executed on the context's designated queue.

---

### What is the difference between Keychain and NSUserDefaults? [Mid]

Both Keychain and NSUserDefaults are persistence mechanisms, but they serve very different purposes:

| Feature | NSUserDefaults | Keychain |
| --- | --- | --- |
| **Primary use** | User preferences, app settings, feature flags | Sensitive credentials: passwords, tokens, keys |
| **Security** | Stored in plaintext in a plist file | Encrypted using AES; hardware-backed on device |
| **Survives app deletion** | ❌ Data is deleted with the app | ✅ Data persists even after app deletion (unless explicitly removed) |
| **Thread safety** | ❌ Not thread-safe | ✅ Thread-safe via system-level locking |
| **iCloud sync** | Optional via `NSUbiquitousKeyValueStore` | Optional via `kSecAttrSynchronizable` |
| **Data size** | Small values (booleans, strings, numbers) | Small secrets (typically under a few KB) |

**Rule of thumb:** Never store passwords, tokens, or private keys in `NSUserDefaults`. Always use the **Keychain** for anything sensitive.

---

### What is Core Data and how does it work? [Mid]

Core Data is an Apple framework used for managing the model layer objects in an application. It provides robust object graph management and persistence solutions.

Key features include:
* **Object Graph Management**: Helps manage a potentially large graph of object instances, bringing them in and out of memory as needed.
* **Relationship Integrity**: Maintains the integrity of relationships and references, ensuring backward and forward links remain consistent.
* **Storage Agnostic**: Core Data abstracts the underlying data store. By default, it uses SQLite, but it can also be configured to store data as an XML file, a binary file, or an in-memory store.

Core Data is highly suitable for managing the "Model" in an MVC architecture.

---

### What are the different options for implementing storage and persistence in iOS? [Mid]

iOS provides various persistence mechanisms ranging from simple to complex, depending on the requirements:

* **In-Memory Storage**: Use arrays, dictionaries, or sets for temporary data that does not need to persist between app launches.
* **UserDefaults & Keychain**: `UserDefaults` is ideal for simple key-value storage (like user preferences). `Keychain` is similar but provides secure, encrypted storage for sensitive data like passwords and tokens.
* **File System (`FileManager`)**: Directly read and write files (e.g., images, JSON, Plists, or custom binary data) to disk using the iOS file system.
* **Object Relational Mapping**: Frameworks like **Core Data** and third-party solutions like **Realm** simplify working with complex object graphs, relationships, and queries.
* **Relational Databases**: For complex querying mechanics without the overhead of Core Data, you can use raw **SQLite** directly.

---

### What is UserDefaults (formerly NSUserDefaults) in iOS? [Easy]

`UserDefaults` provides a simple method to store small amounts of data without requiring a full database, utilizing a **key-value pair system**.
* It offers a programmatic interface for interacting with the default system settings.
* It allows an application to modify its behavior to match a user's preferences (for example, saving a user's preferred media playback speed so it persists across sessions).
* Data saved in `UserDefaults` persists across app launches.

---

### What is NSUserDefaults and what types can it store? [Easy]

`NSUserDefaults` (or `UserDefaults` in Swift) is a key-value store backed by a plist file, designed for persisting small pieces of **user preferences and app settings** across app launches.

**Natively supported types:**
- `String` / `NSString`
- `Int`, `Float`, `Double`, `Bool` (scalar primitives)
- `Data` / `NSData`
- `Date` / `NSDate`
- `Array` / `NSArray` (containing supported types)
- `Dictionary` / `NSDictionary` (with `String` keys and supported values)
- `URL` (Swift only, via special encode/decode)

**Custom types:** Must first be encoded to `Data` using `Codable` / `NSCoding`.

```swift
// Write
UserDefaults.standard.set(true, forKey: "hasSeenOnboarding")
UserDefaults.standard.set("Alice", forKey: "username")

// Read
let seen = UserDefaults.standard.bool(forKey: "hasSeenOnboarding")
let name = UserDefaults.standard.string(forKey: "username")
```

> **Important:** `UserDefaults` is **not thread-safe** as a singleton. Avoid concurrent access from multiple threads without external synchronization.

---

### What is `NSCoding`? [Easy]

`NSCoding` is a protocol that enables an object to be encoded and decoded for archiving and distribution (e.g., saving custom objects to `UserDefaults` or a file).

---

### What is the Keychain in iOS? [Easy]

Keychain is an Apple API for persisting sensitive data (like passwords, keys, and tokens) securely in an iOS app.

---

## SwiftUI

*Apple's declarative UI framework: state management, view composition, animations, and data flow.*

---

### Explain the difference between `.task {}` and `Task {}` in SwiftUI. [Mid]

In SwiftUI, both **`.task {}`** and **`Task {}`** are used to perform asynchronous operations, but they differ in their integration with the view lifecycle.

* **`.task {}` Modifier:**
  * **Lifecycle Integration:** The `.task {}` modifier attaches an asynchronous task directly to a SwiftUI view. This task begins execution when the view appears and is automatically canceled when the view disappears.
  * **Use Case:** Best when the asynchronous operation is closely tied to the view's presence.

* **`Task {}` Initializer:**
  * **Manual Task Creation:** The `Task {}` initializer creates and starts a new asynchronous task independently of the SwiftUI view lifecycle. These tasks are not automatically canceled when a view disappears.
  * **Use Case:** Best when the operation is independent of the view's lifecycle or when initiating tasks outside of a view context.

```swift
// .task {} example
Text(data)
    .task {
        await fetchData()
    }

// Task {} example
Text(data)
    .onAppear {
        Task {
            await fetchData()
        }
    }
```

---

### What is the ButtonStyle protocol in SwiftUI? [Easy]

The `ButtonStyle` protocol in SwiftUI allows developers to create custom, reusable button designs without having to build entirely new views from scratch.

By conforming to `ButtonStyle`, you define a `makeBody(configuration:)` method that determines how the button looks based on its current state (e.g., whether it is being pressed). You can then apply this style to any button using the `.buttonStyle(_:)` modifier, ensuring a consistent UI appearance across your application.

---

### What is the purpose of GeometryReader in SwiftUI? [Mid]

`GeometryReader` is a specialized container view in SwiftUI that provides its child views with information about their size and coordinate space.

It takes up all available space proposed by its parent. Using the `GeometryProxy` object provided in its closure, developers can dynamically read the exact width, height, and safe area insets of the view, making it an essential tool for building complex, responsive custom layouts that adapt to different screen sizes.

---

### How do observable objects announce modifications in SwiftUI? [Mid]

In SwiftUI, observable objects announce modifications using two primary ways: the `@Published` property wrapper or by calling `objectWillChange.send()`:
* **`@Published` property wrapper:** This is a very useful property wrapper in SwiftUI. It allows us to create observable objects that automatically announce when changes occur to the marked properties.
* **`objectWillChange`:** This is a property defined on the `ObservableObject` protocol. Whenever any `@Published` properties of the object change, the compiler synthesizes a default implementation for the property, which emits a value before the object changes. You can also call `objectWillChange.send()` manually to trigger an update.

---

### Why does SwiftUI use structs for views? [Mid]

SwiftUI uses **structs** as the building blocks for views for several strong technical and design reasons:

1. **Performance:** Structs are allocated on the **stack**, not the heap, making creation and destruction significantly faster than class instances. UIKit views (`UIView` subclasses) inherit hundreds of properties and methods; SwiftUI structs contain only what you define.

2. **Immutability & Predictability:** Structs are value types. A SwiftUI view is a **snapshot of state** — a pure description of what the UI should look like at a given moment. When state changes, SwiftUI discards the old struct and creates a new one, eliminating the risk of stale state or unintended side effects.

3. **No Retain Cycles:** Because structs are value types, they don't participate in ARC reference counting. There are no `weak`/`unowned` references to manage, and retain cycles cannot occur in the view layer.

4. **Encourages Functional Design:** Views as structs are inert data — a function of state. This promotes a clean, unidirectional data flow (`State → View`) and discourages mutating behavior inside the view itself.

---

### How does SwiftUI's diffing algorithm optimize UI updates? [Expert]

SwiftUI uses a **state-driven, declarative rendering model** with a built-in diffing engine to update only the parts of the UI that have changed.

**The process:**
1. A state change is triggered (via `@State`, `@ObservedObject`, `@EnvironmentObject`, etc.).
2. SwiftUI re-evaluates the `body` computed property of affected views, producing a **new view tree** (a lightweight value-type tree of view structs).
3. The **diffing engine** compares the **new tree** against the **previously rendered tree**.
4. Only the **minimum necessary changes** are applied to the underlying render layer (backed by the same Core Animation / Metal pipeline as UIKit).

**Why this is efficient:**
- SwiftUI view structs are extremely cheap to create (stack-allocated value types).
- The diffing is performed on the **abstract view description**, not on actual render objects.
- Only genuinely changed subtrees trigger actual layout/render work.

**Helping the diffing engine:**
- Always provide stable, unique `id` values in `ForEach` to help SwiftUI track item identity across updates.
```swift
ForEach(items, id: \.id) { item in
    ItemView(item: item)
}
```

---

### How does SwiftUI's declarative syntax differ from UIKit's imperative approach? [Mid]

The fundamental philosophical difference is **what vs. how**:

- **SwiftUI (Declarative):** You describe **what** the UI should look like for a given state. The framework figures out **how** to render and update it.
- **UIKit (Imperative):** You explicitly describe **how** to manipulate the UI step by step in response to events.

**SwiftUI — declarative:**
```swift
struct ContentView: View {
    @State private var isActive = false

    var body: some View {
        Button(isActive ? "Active" : "Inactive") {
            isActive.toggle()
        }
    }
}
// The label automatically updates when isActive changes — no manual sync needed.
```

**UIKit — imperative:**
```swift
class ViewController: UIViewController {
    var isActive = false
    let button = UIButton(type: .system)

    override func viewDidLoad() {
        super.viewDidLoad()
        button.setTitle("Inactive", for: .normal)
        button.addTarget(self, action: #selector(buttonTapped), for: .touchUpInside)
        view.addSubview(button)
    }

    @objc func buttonTapped() {
        isActive.toggle()
        button.setTitle(isActive ? "Active" : "Inactive", for: .normal) // Must manually sync UI
    }
}
```

| Aspect | SwiftUI | UIKit |
| --- | --- | --- |
| **Style** | Declarative | Imperative |
| **State sync** | Automatic | Manual |
| **Code volume** | Concise | Verbose |
| **Learning curve** | New paradigm | Mature, extensive docs |
| **Availability** | iOS 13+ | iOS 2+ |

---

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
        Button("Tapped \(count) times") { count += 1 }
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
    @Environment(\.colorScheme) var colorScheme   // Built-in
    @Environment(\.dynamicTypeSize) var typeSize   // Built-in

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
// Inject: MyView().environment(\.theme, .dark)
// Read:   @Environment(\.theme) var theme
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
    @Environment(\.horizontalSizeClass) var hSizeClass

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
        Text("Elapsed: \(vm.elapsed)s")
    }
}
```

**When to use:** Any time **this view is the origin** of an observable object (i.e., you write `= ViewModel()` directly). If the object is created outside and passed in, use `@ObservedObject` instead.

---

## SwiftData

*Apple's modern data persistence framework built for Swift and SwiftUI.*

---

## Third-Party Libraries & Dependency Management

*CocoaPods, Carthage, Swift Package Manager, and popular third-party iOS libraries.*

---

### What is CocoaPods? [Easy]

CocoaPods is a dependency manager for Swift and Objective-C Cocoa projects. It is built with Ruby and is installable with the default Ruby available on macOS. The dependencies for your projects are specified in a single text file called a `Podfile`. CocoaPods resolves dependencies, fetches the source code, and links it together in an Xcode workspace.

---

## General Computer Science, OS & Multithreading

*Concurrency (GCD, Operations, async/await), memory management (ARC), algorithms, and OS concepts.*

---

### Is it faster to search for an item in an NSArray or an NSSet? [Mid]

**NSSet** is significantly faster for membership lookups than **NSArray**.

- **NSSet** uses a **hash table** internally. Looking up an object is an O(1) average-case operation because the object's hash value is computed and used to find the bucket directly.
- **NSArray** maintains an **ordered, indexed collection**. A membership search (using `containsObject:`) requires iterating through all elements, giving O(n) time complexity.

**Trade-offs:**

| Feature | NSArray | NSSet |
| --- | --- | --- |
| **Order** | Ordered | Unordered |
| **Duplicates** | Allowed | Not allowed (unique objects only) |
| **Search speed** | O(n) — linear scan | O(1) — hash-based lookup |
| **Index access** | O(1) via index | Not supported |

**Rule of thumb:** Use `NSSet` (or Swift's `Set`) when you need fast membership tests and do not care about order or duplicates. Use `NSArray` (or Swift's `Array`) when order and index-based access matter.

---

### What is the difference between a stack and a heap? [Mid]

A **stack** is a region of memory where data is added or removed in a last-in-first-out (LIFO) order. It is the memory set aside as scratch space for a thread of execution.

Meanwhile, the **heap** is memory set aside for dynamic allocation. Unlike the stack, you can allocate a block at any time and free it at any time.

*Note: In Objective-C, all objects are always allocated on the heap, or at least should be treated as if on the heap.*

---

### What is the difference between synchronous and asynchronous tasks in iOS? [Easy]

* **Synchronous tasks** block the current thread of execution. You must wait for the task to finish completely before the program can move on to the next line of code.
* **Asynchronous tasks** execute in the background, allowing the current thread to continue running without waiting. The task completes independently without blocking the application's flow and can send a notification when the task is complete.

---

### What is Grand Central Dispatch (GCD) and how is it used? [Mid]

**Grand Central Dispatch (GCD)** is a low-level C API that allows developers to run tasks concurrently. It provides and manages queues of tasks in an iOS app, efficiently managing background threads and abstracting away complex thread management code.

Benefits of using GCD include:
* **Responsiveness:** Improves app responsiveness by deferring computationally expensive tasks to run in the background.
* **Concurrency:** Provides an easier concurrency model than locks and threads, helping to avoid concurrency bugs.
* **Performance:** Optimizes code with higher performance primitives for common patterns.

GCD is commonly used to manage concurrent code and execute operations asynchronously. For example, network calls are often performed on a background thread while UI updates are dispatched back to the main thread.

---

### What is the difference between serial and concurrent queues? [Easy]

* **Serial** queues execute tasks one at a time, ensuring that only one task runs at any given moment in the order they were added.
* **Concurrent** queues allow multiple tasks to be executed simultaneously. Tasks are still started in the order they are added, but they can finish at different times.

---

### What is a race condition? [Mid]

A **race condition** occurs when two or more threads access shared mutable state **concurrently**, and the final outcome depends on the unpredictable scheduling order of those threads. The result is **non-deterministic** and can produce data corruption, crashes, or subtle bugs that are very hard to reproduce.

**Example:**
```swift
var counter = 0

DispatchQueue.global().async { counter += 1 } // Thread A
DispatchQueue.global().async { counter += 1 } // Thread B
// Final value of counter is unpredictable (could be 1 or 2)
```

**Solutions:**
- **Serial DispatchQueue:** Funnel all access through a single serial queue.
- **Concurrent queue + `.barrier`:** Allow concurrent reads, but serialize writes.
- **NSLock / os_unfair_lock:** Mutual exclusion locks.
- **Actors (Swift 5.5+):** The compiler enforces serial access to actor-isolated state, eliminating data races at compile time.

---

### What is Quality of Service (QoS) in GCD? [Mid]

**Quality of Service (QoS)** is a hint you provide to the system about the relative priority and urgency of the work you are dispatching. The system uses this to prioritize thread scheduling, CPU time, and energy consumption.

| QoS Class | Priority | Use Case |
| --- | --- | --- |
| `.userInteractive` | Highest | Animations, direct UI updates. Work must complete immediately. |
| `.userInitiated` | High | Work the user explicitly triggered (e.g., opening a document). Results needed within seconds. |
| `.default` | Medium | General-purpose work not classified by the developer. |
| `.utility` | Low | Long-running tasks with visible progress (e.g., downloading a file). |
| `.background` | Lowest | Maintenance, prefetching, backups. User is unaware this work is happening. |
| `.unspecified` | Legacy | No QoS information; the system infers from the thread's environment. |

```swift
DispatchQueue.global(qos: .userInitiated).async {
    let data = fetchDataFromAPI() // High priority
    DispatchQueue.main.async {
        self.updateUI(with: data) // Back on main thread
    }
}
```

---

### What is Functional Programming? [Mid]

Functional programming is a declarative programming paradigm, much like Object-Oriented Programming (OOP) is an imperative one. In OOP, you write code that tells the computer *how* to perform a specific task step-by-step. In contrast, functional programming focuses on telling the computer *what* to do by evaluating mathematical-style functions. It emphasizes immutability, pure functions (functions without side effects), and higher-order functions.

---

### What is an asynchronous event? [Easy]

An asynchronous event is an operation or task that runs independently of the main program flow. Instead of blocking the current thread and waiting for the task to finish, the program can continue executing other code. When the asynchronous task completes, it notifies the system (often via a callback, closure, or delegate), allowing the program to handle the result or update the UI. Common examples include network requests, file I/O operations, and background computations.

---

### What is Test-Driven Development (TDD) and Behavior-Driven Development (BDD)? [Mid]

Both are software development methodologies that emphasize writing tests, but they differ in their approach and scope:
* **Test-Driven Development (TDD):** A process where test cases are written to define the desired software characteristics *before* the actual code is written. Developers create a failing unit test for a specific functionality, write the minimum amount of bug-free code required to pass that test, and then refactor the code. It focuses heavily on code quality, architectural design, and developer-level specifications.
* **Behavior-Driven Development (BDD):** An extension of TDD that focuses on the behavior of the application from the end-user's perspective. BDD uses human-readable, domain-specific language (often structured as Given-When-Then) to define system behavior. This bridges the communication gap between developers, QA, and non-technical stakeholders to ensure the software meets business requirements.

---

### What is Regression in software testing? [Easy]

Regression occurs when a modification made to the codebase unintentionally alters or breaks previously working functionality. In testing, a "regression failure" happens when an existing passing test case suddenly fails after new changes (such as bug fixes or new features) are integrated. Automated unit and UI tests act as a critical safety net to catch regressions immediately, ensuring that core app behavior remains intact over time.

---

### What is an overlay in the context of operating systems and memory management? [Expert]

An overlay is a memory management technique used when a program is larger than the available physical memory.

Instead of loading the entire program into memory at once, the program is divided into logical, self-contained sections called overlays. Only the required portions of the program are loaded into memory at any given time. As the program executes, different overlays are dynamically swapped in and out of the same memory space. While largely obsolete in modern systems due to the advent of virtual memory, it remains a fundamental concept in computing history.

---

### What is a Regular Expression? [Easy]

**Regular Expressions** (Regex) are special string patterns that dictate how to search for a string.
* They consist of a sequence of characters that specifies a precise **search pattern** in text.
* They are heavily used to perform **find** or **find-and-replace** operations on strings, and to validate data formats.

---

### What is processor management in operating systems? [Mid]

**Processor management** is a core operating system function that handles the allocation of the CPU to different processes.
* It provides the tools and resources to steer processes toward better performance.
* It ensures that each process and application receives **enough of the processor's time** to function properly.
* It also handles the **deallocation** of the processor after a process is completed or interrupted.

---

### How does process and thread management work in iOS? [Mid]

In iOS, **process management** heavily relies on threading to execute tasks.
* Every application in iOS starts with a **single main thread** that runs the application's primary functions and UI updates.
* Each thread in iOS serves as a **single path of execution**.
* Developers use concurrency APIs like Grand Central Dispatch (GCD) or Swift Concurrency to manage multiple threads and perform background operations efficiently.

---

### What is the difference between atomic and non-atomic properties in Objective-C? [Mid]

In Objective-C, `atomic` and `nonatomic` are property attributes that control thread-safety of synthesized accessor methods.

- **`atomic` (default):** The synthesized getter and setter are wrapped in a lock, guaranteeing that a complete value is always returned or set — even if multiple threads access the property simultaneously. However, this comes at a performance cost.
- **`nonatomic`:** No locking is performed. Accessors are faster, but simultaneous reads and writes from different threads can result in **partial values** or undefined behavior.

```objective-c
@property (atomic, strong)    NSString *threadSafeTitle;   // Safe, but slower
@property (nonatomic, strong) NSString *fastTitle;          // Fast, but not thread-safe
```

> **Note:** `atomic` does **not** make a property fully thread-safe in all situations (e.g., an array being mutated while being iterated). It only guarantees atomicity of a single read or write operation. For compound operations, explicit locking (NSLock, serial queues, etc.) is still required.

In Swift, there is no `atomic` keyword — all stored properties are `nonatomic` by default. Thread safety must be implemented explicitly using `DispatchQueue`, `NSLock`, or Swift `actor` types.

---

### What are the main mechanisms for achieving concurrency in iOS? [Mid]

iOS provides three primary concurrency mechanisms:

1. **POSIX Threads (`Thread`):** Low-level, manual thread management. You create and manage threads yourself. Rarely used directly in modern iOS development.

2. **Grand Central Dispatch (GCD):** A C-based API built on top of threads. You submit **blocks (closures)** to **dispatch queues** (serial or concurrent), and the system manages the underlying thread pool automatically. This is the most common approach.

3. **Operation Queues (`Operation` / `OperationQueue`):** An object-oriented abstraction over GCD. `Operation` objects can be paused, cancelled, have dependencies, and observe state using KVO. Best for complex task graphs with interdependencies.

4. **Swift Concurrency (`async`/`await`, `Task`, `Actor`) — Swift 5.5+:** The modern, first-party concurrency system. Provides structured concurrency with cooperative thread pooling, compile-time data-race safety via `actor` isolation, and a readable linear code style.

```swift
// GCD example
DispatchQueue.global(qos: .userInitiated).async {
    let result = performHeavyWork()
    DispatchQueue.main.async { self.updateUI(result) }
}

// async/await example
Task {
    let result = await performHeavyWork()
    await MainActor.run { self.updateUI(result) }
}
```

---

### What is an Autorelease Pool and when should you use one? [Expert]

An **autorelease pool** is a memory management mechanism (from Objective-C's manual reference counting era) that defers the release of objects until the pool is drained. Objects sent `autorelease` are not freed immediately; instead they are added to the pool's queue and released all at once when the pool is drained.

With **ARC**, the compiler inserts `retain`/`release` calls automatically. You rarely interact with autorelease pools directly, but there are still scenarios where they are useful in Swift.

**Why it still matters:**
Each iteration of the main run loop is wrapped in an autorelease pool. However, when you create a large number of short-lived objects in a **tight loop on a background thread**, memory can accumulate between pool drains.

**Solution — use `autoreleasepool` block:**
```swift
for imageURL in thousandsOfURLs {
    autoreleasepool {
        let image = UIImage(contentsOfFile: imageURL.path)
        processImage(image) // image is released at end of each iteration
    }
}
```
Without the `autoreleasepool` block, all `UIImage` objects would remain in memory until the outer pool is drained, potentially causing memory spikes or out-of-memory crashes.

**In Objective-C (pre-ARC), the syntax was:**
```objective-c
@autoreleasepool {
    // temporary objects released here
}
```

---

### What is Automatic Reference Counting (ARC)? [Mid]

**ARC (Automatic Reference Counting)** is the compiler-level memory management system used in both Swift and Objective-C. The compiler automatically inserts `retain` and `release` calls at compile time — you do not manually manage memory.

**How it works:**
- Every class instance has a **reference count**.
- When a **strong reference** is created (e.g., assigning to a variable), the count **increases by 1**.
- When that reference goes out of scope or is set to `nil`, the count **decreases by 1**.
- When the reference count reaches **0**, the object is **immediately deallocated** from the heap.

```swift
class Person {
    let name: String
    init(name: String) { self.name = name }
    deinit { print("\(name) is being deallocated") }
}

var ref1: Person? = Person(name: "Alice") // ref count = 1
var ref2 = ref1                            // ref count = 2
ref1 = nil                                 // ref count = 1
ref2 = nil                                 // ref count = 0 → deallocated
```

**Key concern — Retain Cycles:**
If two objects hold strong references to each other, their reference counts never reach zero and they are never deallocated, causing a **memory leak**. This is solved using `weak` or `unowned` references for one side of the relationship.

---

### What is Code Coverage? [Easy]

Code coverage is a software testing metric that measures the percentage of source code statements executed during automated testing. A program with high code coverage has had a large portion of its logic verified by tests, suggesting a lower probability of containing undetected software bugs compared to a program with low test coverage.

---

### What are the different kinds of operations possible on a semaphore? [Mid]

A semaphore relies on two primary atomic operations to manage thread synchronization:
* **Wait():** Decrements the semaphore value by 1. If the value is already 0, the thread attempting the wait operation is blocked until the value becomes greater than 0.
* **Signal():** Increments the semaphore value by 1. If other threads were blocked waiting on this semaphore, one of those threads is unblocked and permitted to proceed.

---

### What is a Real-Time Operating System (RTOS)? [Mid]

**RTOS** stands for Real-Time Operating System. It is engineered specifically for applications subjected to strict time constraints, where data processing must occur flawlessly within rigid deadlines (often measured in tenths of seconds). It is heavily used in systems interacting dynamically with external hardware events.

---

### What are two common types of process synchronization? [Mid]

* **Interprocess Communication (IPC):** Mechanisms that allow distinct processes to communicate and synchronize their state (e.g., shared memory, message passing).
* **Mutual Exclusion (Mutex):** Techniques designed to ensure that only a single process or thread can access a shared resource or critical section of code at any given time (e.g., locks, binary semaphores).

---

### What is the difference between `weak` and `unowned` references? When should you use each? [Mid]

Both `weak` and `unowned` prevent a reference from incrementing an object's ARC retain count, which is essential for **breaking retain cycles**.

| | `weak` | `unowned` |
| --- | --- | --- |
| **Type** | Always **optional** (`T?`) | **Non-optional** (`T`) |
| **Becomes nil?** | ✅ Yes — automatically set to `nil` when the object is deallocated | ❌ No — the reference is **not zeroed out** |
| **Safety** | Safe — you check for `nil` before use | **Crashes** if accessed after the referenced object is deallocated |
| **Use when** | The referenced object has an **equal or shorter** lifetime | The referenced object is **guaranteed to outlive** the reference holder |

**When to use `weak`:**
```swift
class ViewController: UIViewController {
    var viewModel: ViewModel?
}
class ViewModel {
    weak var delegate: ViewControllerDelegate? // Delegate may be deallocated first
}
```

**When to use `unowned`:**
```swift
class Customer {
    var card: CreditCard?
}
class CreditCard {
    unowned let customer: Customer // A card cannot exist without a customer
    init(customer: Customer) { self.customer = customer }
}
```

**In closures:**
- Use `[weak self]` when `self` might be `nil` by the time the closure executes.
- Use `[unowned self]` only when you are certain `self` will still be alive (e.g., in a closure used for a view's button action that cannot outlive the view controller).

---

### Why must you capture `self` explicitly in asynchronous closures? [Mid]

In Swift, closures capture and **retain** values from their surrounding context. When a closure is dispatched asynchronously (e.g., on a background queue), it may execute **after** the enclosing scope has returned. If `self` is a class instance, capturing it **strongly** ensures it stays alive for the duration of the closure — but this can also create retain cycles.

**Why explicit capture:**
- Asynchronous closures can outlive the scope in which they were created.
- Swift requires you to write `self.` or use `[self]` in escaping closures as a **conscious acknowledgement** that you are extending the lifetime of `self`.
- This prevents accidental captures and makes the retain graph explicit.

**Best practices:**
```swift
// Retain cycle risk (avoid in delegates/long-lived objects)
urlSession.dataTask(with: url) { [weak self] data, _, _ in
    guard let self else { return }  // Safe — self could have been deallocated
    self.updateUI(with: data)
}

// Unowned — only when self is guaranteed to outlive the closure
urlSession.dataTask(with: url) { [unowned self] data, _, _ in
    self.updateUI(with: data)  // Crashes if self was deallocated
}
```

---

### Where should we perform UI tasks in GCD? [Easy]

The **Main Queue** is perfect for updating the UI and handling user interactions, whereas any other heavy or long-running tasks should run on a **Background Thread**.

```objective-c
dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
    // Load your data here in the background.
    dispatch_async(dispatch_get_main_queue(), ^{
        // Update UI on the main thread.
    });
});
```

---

### What is the HTTP protocol and what are its common methods? [Easy]

HTTP is the application protocol, or set of rules, that websites use to transfer data from the web server to a client.

* **GET:** Used to retrieve data without altering any data on the server.
* **HEAD:** Identical to GET but only sends back the headers and none of the actual data.
* **POST:** Used to send data to the server, commonly used when filling out a form.
* **PUT:** Used to send or replace data at a specific location.
* **DELETE:** Deletes data from the specific location provided.

---

### What are the differences between GCD and `NSOperation`? [Mid]

- **GCD (Grand Central Dispatch)**: A low-level C-based API that is lightweight, simple, and uses lock-free algorithms. Best for simple cases where you want less overhead to quickly dispatch work to the background.
- **`NSOperation` and `NSOperationQueue`**: Objective-C classes providing an object-oriented wrapper over GCD.

**Advantages of NSOperation over GCD**:
- **Control**: You can pause, cancel, and resume an `NSOperation`.
- **Dependencies**: You can set up dependencies between multiple operations.
- **State Monitoring**: You can monitor the state (`ready`, `executing`, `finished`).
- **Concurrency Limits**: Specify the maximum number of queued operations that can run simultaneously.
- **Observability**: Properties can be observed using KVO.

---

### What is the difference between static and dynamic typing? [Mid]

- **Static typing**: Type checking occurs at compile time. You must define a type for variables, and operations are validated by the compiler.
- **Dynamic typing**: Type checking occurs at runtime. You will get runtime errors if trying to perform operations on incompatible types, but it provides the benefit of writing versatile functions that handle multiple data types.

---

### What is the difference between SVN and Git? [Easy]

- **SVN (Subversion)**: Relies on a centralized system for version management. It has a central repository where working copies are generated, and a network connection is always required for access and commits.
- **Git**: Relies on a distributed system. You have a local repository on which you can work and commit offline; a network connection is only required to synchronize (push/pull) with the remote repository.

---

### What is the difference between JSON and XML? [Easy]

- **JSON (JavaScript Object Notation)**: Lighter weight, uses JavaScript object syntax (key-value pairs and arrays), and is easier to parse natively in most modern frameworks.
- **XML (eXtensible Markup Language)**: Heavier, uses markup tags (like HTML), supports attributes, and is generally more verbose.

---

### What is the difference between REST and SOAP? [Easy]

- **REST (Representational State Transfer)**: An architectural style utilizing standard HTTP methods (GET, POST, PUT, DELETE). It typically uses lightweight formats like JSON.
- **SOAP (Simple Object Access Protocol)**: A strict protocol that relies exclusively on XML for messaging and often requires more bandwidth and overhead.

---

### What is the difference between Stack and Heap memory? [Mid]

- **Stack**: Fast access, space managed efficiently by the CPU. Memory does not become fragmented, and variables are automatically deallocated when they go out of scope. There is an OS-dependent limit on stack size.
- **Heap**: Slower access, used for dynamic memory allocation. Variables can be accessed globally and have no strict memory limit (other than physical RAM). Memory can become fragmented over time, and developers must manage it (via ARC in Swift/Objective-C).

---

### What are the core concepts of Object-Oriented Programming (OOP)? [Easy]

The core concepts of Object-Oriented Programming (OOP) include:
1. **Abstraction**
2. **Encapsulation**
3. **Inheritance**
4. **Polymorphism**
5. **Composition, Aggregation, and Association**

---

### What is the difference between composition, aggregation, and association in object-oriented programming? [Mid]

- **Composition** implies a relationship where the child cannot exist independently of the parent. 
  - *Example:* A House (parent) and a Room (child). Rooms don't exist separate from a House.
- **Aggregation** implies a relationship where the child can exist independently of the parent. 
  - *Example:* A Class (parent) and a Student (child). If you delete the Class, the Students still exist.
- **Association** is a "relates-to" relationship between two objects, where one object is related to another without relying on composition or aggregation. 
  - *Example:* A student may take a course. The student and the course are related, but neither is a part of the other.

---

### What are the common algorithms used for array searching, and how do they differ? [Mid]

Common algorithms used to search for elements or indexes in an array include:
- **Linear Search:** A sequential search algorithm that starts at one end and goes through each element of a list until the desired element is found. If not found, it continues until the end of the dataset. It has a time complexity of `O(N)`.
- **Binary Search:** A more efficient algorithm that requires the array or list to be sorted. It repeatedly divides the search interval in half to find the desired element. It has a time complexity of `O(log N)`.
- **Ternary Search:** A divide-and-conquer algorithm that is similar to binary search but divides a sorted array into three parts instead of two. It has a time complexity of `O(log3 N)`.

---

### What are the main categories and types of data structures? [Easy]

Data structures generally fall into these categories:
- **Linear (Static):** Arrays.
- **Linear (Dynamic):** Linked lists (nodes and next pointers), Stacks (LIFO), and Queues (FIFO).
- **Non-linear:** Graphs (edges and vertices, where multiple edges can connect nodes) and Trees (edges and vertices with a hierarchical structure).

---

### What does 'thread-safe' mean? [Mid]

**Thread-safe** code is code that functions correctly and predictably when accessed concurrently by multiple threads simultaneously. A piece of code is thread-safe if it:

- Produces **correct, consistent results** regardless of the execution order of threads.
- Does not suffer from **data races** (two threads reading/writing shared data simultaneously without synchronization).
- Does not cause **deadlocks** (two threads indefinitely waiting for each other to release a lock).

**Making code thread-safe in Swift:**

1. **Serial DispatchQueue:** Serialize all access through a single queue.
2. **Concurrent Queue + `.barrier`:** Allow concurrent reads, but serialize writes.
3. **NSLock / os_unfair_lock:** Low-level mutual exclusion.
4. **`actor` (Swift 5.5+):** The compiler enforces that only one task accesses actor-isolated state at a time.

```swift
actor SafeCounter {
    private var value = 0
    func increment() { value += 1 }
    func getValue() -> Int { return value }
}
```

---
