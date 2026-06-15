import json
import os

processed_data = [
    {
        "category": "Core Data & Persistence",
        "question": "What is Core Data? [Easy]",
        "answer": "Core Data is a framework used to manage model layer objects. It provides the ability to persist object graphs to a persistent store. Data is organized into a relational entity-attribute model."
    },
    {
        "category": "Core Data & Persistence",
        "question": "When would you use Core Data over NSUserDefaults? [Easy]",
        "answer": "**NSUserDefaults** is typically used to store small bits of data, such as simple settings and user preferences.\n\n**Core Data** is used to store larger lists of elements, manage relationships between objects, and persist complex object graphs."
    },
    {
        "category": "Core Data & Persistence",
        "question": "What is a managed object context? [Mid]",
        "answer": "A managed object context is an instance of `NSManagedObjectContext`. It serves as the central object in the Core Data stack and acts as an in-memory scratchpad. It is used to create, fetch, and save managed objects, as well as to manage undo and redo operations. \n\nWhile it is possible to have multiple managed object contexts, there is typically at most one managed object instance representing any given record in a persistent store per context."
    },
    {
        "category": "Core Data & Persistence",
        "question": "What is NSFetchRequest? [Easy]",
        "answer": "`NSFetchRequest` is the class responsible for fetching data from Core Data. Fetch requests can be configured with predicates and sort descriptors to fetch a specific set of objects meeting certain criteria, retrieve individual values, and more."
    },
    {
        "category": "iOS Fundamentals",
        "question": "What are some ways of debugging in iOS? [Easy]",
        "answer": "There are several tools and techniques available for debugging in iOS:\n\n*   **Console Output**: `NSLog` and `print` functions can be used to output information directly into the console.\n*   **Breakpoints**: Breakpoints can be set in Xcode to pause execution, allowing developers to inspect the current state using the Debug bar and Variables view.\n*   **Advanced Tools**: Senior developers often rely on advanced tools such as **Instruments** (for memory leaks, performance profiling, etc.) and **Crash Logs** to diagnose and fix complex issues."
    },
    {
        "category": "Design Patterns & Architecture",
        "question": "What is a Singleton pattern, and how can you make it thread-safe in Swift? [Mid]",
        "answer": "A **Singleton** is a design pattern that ensures **only one instance** of a class is created and provides a **global access point** to that instance. This is useful when exactly one object is needed to coordinate actions across the system, such as a **shared database manager, network manager, or user session handler**.\n\nIn Swift, a Singleton is typically implemented using a **static instance** inside the class, which automatically uses lazy initialization and is thread-safe for creation.\n\n```swift\nclass DatabaseManager {\n    // Singleton instance. The static keyword ensures it belongs to the class.\n    static let shared = DatabaseManager() \n    \n    // Prevents direct instantiation of the class from outside.\n    private init() { \n        print(\"DatabaseManager initialized\") \n    }\n    \n    func fetchData() {\n        print(\"Fetching data...\")\n    }\n}\n```\n\n**Use Cases for Singleton**\n*   **Network Manager**: API requests (`URLSession.shared`)\n*   **Database Access**: Core Data or Firebase (`DatabaseManager.shared`)\n*   **User Session**: Managing logged-in user state\n*   **Logging System**: Application-wide logging service\n\n**Pros & Cons of Singleton Pattern**\n*   **Pros**: Ensures a single instance, easy to access globally, efficient resource usage.\n*   **Cons**: Can introduce hidden dependencies, harder to unit test, can lead to tight coupling.\n\n**Thread Safety in Swift**\nWhen working in a multithreaded environment, ensuring that a singleton instance's methods and properties are thread-safe is crucial. This can be achieved using `DispatchQueue`.\n\n*Approach 1: Using a Serial Dispatch Queue (`sync`)*\nEnsures that only **one thread accesses the critical section at a time**.\n\n```swift\nclass ThreadSafeSingleton {\n    static let shared = ThreadSafeSingleton()\n    private init() { }\n    \n    private let queue = DispatchQueue(label: \"SingletonQueue\")\n\n    func safeMethod() {\n        queue.sync {\n            print(\"Thread-safe operation\")\n        }\n    }\n}\n```\n\n*Approach 2: Using a Concurrent Queue with Dispatch Barrier (`.barrier`)*\nOptimized for **read-heavy** operations where multiple threads can **read simultaneously**, but **writes remain exclusive**.\n\n```swift\nclass ThreadSafeSingleton {\n    static let shared = ThreadSafeSingleton()\n    private init() { }\n    \n    private let queue = DispatchQueue(label: \"LoggerQueue\", attributes: .concurrent)\n    private var logDict: [String: Any] = [:]\n\n    func writeToLog(key: String, value: Any) {\n        queue.async(flags: .barrier) { [weak self] in\n            self?.logDict[key] = value\n        }\n    }\n    \n    func readFromLog(key: String) -> Any? {\n        queue.sync {\n            return logDict[key]\n        }\n    }\n}\n```"
    },
    {
        "category": "Design Patterns & Architecture",
        "question": "What is the delegation pattern? [Mid]",
        "answer": "The delegation pattern is a powerful structural design pattern heavily used in building iOS applications. \n\nThe basic idea is that one object acts on behalf of, or in coordination with, another object. The delegating object typically keeps a reference to the other object (the **delegate**) and sends a message to it at an appropriate time (e.g., when an event occurs or data is needed).\n\nIt is important to note that they usually have a **one-to-one relationship**, and the delegate reference should typically be declared as `weak` to prevent retain cycles and memory leaks."
    },
    {
        "category": "Design Patterns & Architecture",
        "question": "What is the MVC architecture pattern? [Easy]",
        "answer": "MVC stands for **Model-View-Controller**. It is Apple\u2019s main software design pattern for developing iOS applications and implementing user interfaces.\n\nMVC consists of three distinct layers:\n*   **Model**: Represents the data and business logic for the application (e.g., persistence, networking, model objects).\n*   **View**: Brings things to the screen. It displays UI elements like buttons and text. The view layer does not know anything about the model layer, and vice versa.\n*   **Controller (View Controller)**: Manages the flow of data between the model and the view. All communication between the model and the view is orchestrated by the controller.\n\n**The \"Massive View Controller\" Problem**\nWhile MVC is good for general-purpose design, strictly using it often leads to the \"Massive View Controller\" problem. This occurs when excessive logic and responsibilities (like networking, data formatting, and complex state management) are pushed into View Controllers. As a result, the code becomes rigid, bloated, and difficult to test. To remedy this, developers often adopt alternative design patterns such as MVP, MVVM, or VIPER."
    },
    {
        "category": "Design Patterns & Architecture",
        "question": "What is MVVM? [Mid]",
        "answer": "MVVM stands for **Model-View-ViewModel**. It is a software architecture pattern used for implementing user interfaces.\n\nMVVM is an augmented version of MVC where the presentation logic is moved out of the controller and into a dedicated **ViewModel**. \n\nThe ViewModel is responsible for handling most, if not all, of the view's display logic and state transformations. By extracting this logic, MVVM significantly shrinks the size of the View Controller. This makes the codebase much easier to read, follow, and unit test, directly addressing the \"Massive View Controller\" problem commonly encountered in standard MVC."
    },
    {
        "category": "UIKit",
        "question": "What considerations do you need when writing a UITableViewController which shows images downloaded from a remote server? [Mid]",
        "answer": "When displaying remotely downloaded images in a `UITableViewController`, you should consider the following best practices:\n\n*   **Lazy Loading**: Only trigger the image download when the cell is about to be displayed on the screen (e.g., inside `tableView(_:cellForRowAt:)` or `tableView(_:willDisplay:forRowAt:)`).\n*   **Asynchronous Downloading**: Download the image asynchronously on a background thread. This prevents the main UI thread from blocking, ensuring the user can scroll smoothly.\n*   **Cell Reusability Check**: Because table view cells are reused, by the time an image download completes, the cell might have been recycled for a different row. Always verify that the downloaded image matches the data currently represented by the cell before displaying it.\n*   **Main Thread UI Updates**: Once the image is successfully downloaded and validated, ensure that you switch back to the main thread to update the `UIImageView`.\n*   **Caching**: Implement an image caching mechanism (e.g., `NSCache` or a third-party library like SDWebImage) to avoid repeatedly fetching the same images over the network."
    },
    {
        "category": "Swift Fundamentals",
        "question": "What is a protocol? How do you define your own protocol? [Easy]",
        "answer": "A **protocol** defines a blueprint of required and optional methods, properties, and other requirements that suit a particular task or piece of functionality. \n\nAny class, struct, or enum is allowed to adopt a protocol and provide an actual implementation of those requirements. This allows other objects to interact with the adopting types through the protocol interface without needing to know their specific concrete types.\n\nAn example of how a protocol is defined in Swift:\n\n```swift\nprotocol MyCustomDataSource: AnyObject {\n    var numberOfRecords: Int { get }\n    func record(at index: Int) -> [String: Any]\n}\n```\n\n*Note: In Swift, optional methods can be achieved by marking the protocol with `@objc` and the methods with `@objc optional`, or more commonly, by providing default implementations via protocol extensions.*\n\nA very common use case for protocols in iOS is providing a DataSource or Delegate for UI components like `UITableView` or `UICollectionView`."
    },
    {
        "category": "General Computer Science, OS & Multithreading",
        "question": "What are the differences between Waterfall and Agile methodologies? [Easy]",
        "answer": "**Waterfall methodology** is a rigid, sequential model for software development. It progresses through pre-defined phases: feasibility, planning, design, build, test, production, and support.\n\n**Agile methodology** is an iterative and flexible approach that focuses on continuous delivery, allowing for changing project requirements along the way.\n\n**Key Differences:**\n*   **Process Structure**: Waterfall strictly separates development into sequential phases. Agile breaks the project down into short, iterative cycles known as sprints.\n*   **Project Scope**: Waterfall treats the lifecycle as one massive project. Agile treats it as a collection of many smaller projects, continuously evolving based on feedback.\n*   **Adaptability**: In Waterfall, requirements must be fully established beforehand, with little room for mid-project changes. Agile is highly flexible and welcomes changing requirements at any time.\n*   **Testing Phase**: In Waterfall, testing occurs strictly after the build phase is complete. In Agile, testing is performed concurrently with development during each sprint.\n*   **Customer Involvement**: Waterfall is largely an internal process without ongoing client input. Agile relies heavily on frequent user and stakeholder feedback to improve customer satisfaction."
    },
    {
        "category": "Swift Fundamentals",
        "question": "What is the difference between a class and an object? [Easy]",
        "answer": "In object-oriented programming, a **class** is a blueprint or template that defines the properties (attributes) and behaviors (methods) common to a specific type of entity.\n\nAn **object**, on the other hand, is an actual **instance** of a class. It is created in memory during runtime and holds its own specific state based on the blueprint provided by its class."
    },
    {
        "category": "General Computer Science, OS & Multithreading",
        "question": "What is JSON? What are its pros and cons? [Easy]",
        "answer": "JSON stands for **JavaScript Object Notation**. It is a lightweight, human-readable data-interchange format that uses plain text to transmit data objects consisting of attribute-value pairs and arrays.\n\n**Pros:**\n*   **Lightweight**: It is significantly less verbose than XML, meaning it can represent the same data in fewer bytes. This results in faster network transmissions and reduced parsing overhead.\n*   **Wide Compatibility**: It is easy to parse, natively supported by JavaScript, and has excellent tooling across almost all modern programming languages (such as `Codable` in Swift).\n\n**Cons:**\n*   **No Comments**: Unlike XML, JSON does not natively support comments, which can make documenting configuration files difficult.\n*   **Limited Data Types**: JSON only supports basic types (strings, numbers, booleans, arrays, objects, and null). It lacks built-in support for complex types like dates or binary data, which must be serialized into strings or numbers."
    },
    {
        "category": "iOS Fundamentals",
        "question": "What are the different execution states of an iOS application, and how does it transition between them? [Mid]",
        "answer": "An iOS application transitions through several execution states during its lifecycle:\n\n*   **Not Running**: The application has not yet been launched by the user, or it was previously running but has been entirely terminated by the operating system to reclaim memory.\n*   **Inactive**: The application is running in the foreground but is not currently receiving events. This typically happens briefly during state transitions, or when handling system interruptions like an incoming phone call or SMS.\n*   **Active**: The application is running in the foreground and actively receiving user events. This is the normal operating mode for foreground apps.\n*   **Background**: The application is running in the background and executing code. Most apps enter this state briefly on their way to being suspended. Apps that request extra execution time or support background modes (e.g., audio playback, location updates) may remain in this state longer.\n*   **Suspended**: The application is retained in memory in the background but is completely paused and not executing any code. The system may silently purge suspended applications at any time to free up memory for active foreground apps.\n\n**Transition Example:**\nWhen launched, an app transitions from **Not Running** \u2192 **Inactive** \u2192 **Active**. If the user returns to the Home screen, it transitions to **Inactive** \u2192 **Background**, and eventually settles into a **Suspended** state."
    },
    {
        "category": "Objective-C",
        "question": "Is it faster to search for an item in an NSArray or an NSSet? [Easy]",
        "answer": "Searching for an item is generally much faster in an **`NSSet`** than in an **`NSArray`**.\n\n*   **`NSSet`**: Uses hash values to store and retrieve items, providing an average $O(1)$ time complexity for lookups. However, it is an unordered collection and guarantees that it holds at most one instance of any given object.\n*   **`NSArray`**: Stores items sequentially. Searching for an item requires iterating through its contents, resulting in an average $O(n)$ time complexity. Its advantage is that it maintains a specific order and allows duplicate objects."
    }
]

file_path = '/Users/moca/Documents/Coding/iOS Interview Questions/batches/processed_batch_0.json'
with open(file_path, 'w') as f:
    json.dump(processed_data, f, indent=2)

print(f"Successfully processed batch and saved to {file_path}")
