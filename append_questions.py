import json

data = [
  {
    "category": "Swift Language & Concurrency",
    "question": "Completion Handler vs Task: A comparison of legacy callback-based approaches versus modern async/await structured concurrency, including reference capture and retain cycle risks.",
    "answer": "Completion handlers are legacy callback-based patterns where you pass a closure to be executed when an asynchronous operation finishes. They often suffer from nested callbacks ('pyramid of doom') and require careful management of `self` captures to avoid retain cycles. `Task` and async/await represent modern structured concurrency in Swift. They allow writing asynchronous code sequentially, automatically manage thread execution, and generally avoid retain cycles since they don't inherently strongly capture `self` in the same way escaping closures do, leading to cleaner and safer code."
  },
  {
    "category": "Swift Language & Concurrency",
    "question": "Variadic Functions: What is a variadic function in Swift and how do you use the ... syntax?",
    "answer": "A variadic function is a function that accepts zero or more values of a specified type. You denote a variadic parameter by inserting three periods (`...`) after the parameter's type name. Inside the function body, the variadic parameter is made available as an array of the appropriate type. For example, `func sum(numbers: Int...)` allows you to call `sum(numbers: 1, 2, 3)`."
  },
  {
    "category": "Swift Language & Concurrency",
    "question": "Advanced Set Operations: Detailed implementation examples for intersection, subtracting, isDisjoint, union, symmetricDifference, isSubset, and isSuperset.",
    "answer": "Swift's `Set` provides mathematically sound operations:\n- `intersection(_:)`: Creates a new set with elements common to both sets.\n- `subtracting(_:)`: Creates a new set with elements not in the specified set.\n- `isDisjoint(with:)`: Returns true if the two sets have no elements in common.\n- `union(_:)`: Creates a new set with all elements from both sets.\n- `symmetricDifference(_:)`: Creates a new set with elements in either set, but not both.\n- `isSubset(of:)`: Returns true if all elements are contained in the specified set.\n- `isSuperset(of:)`: Returns true if the set contains all elements of the specified set."
  },
  {
    "category": "General Frameworks & Tooling",
    "question": "Cocoa vs. Cocoa Touch: What is the difference between these two application frameworks?",
    "answer": "Cocoa is the application framework for macOS development. It includes the Foundation and AppKit frameworks. Cocoa Touch is the application framework for iOS, iPadOS, watchOS, and tvOS development. It includes the Foundation and UIKit frameworks. The primary difference lies in the UI layer (AppKit for macOS, UIKit for iOS/iPadOS)."
  },
  {
    "category": "General Frameworks & Tooling",
    "question": "UI Automation API: Which API is suitable for writing test scripts to interact with the application’s UI elements?",
    "answer": "XCTest is the primary framework provided by Apple for UI Automation. Specifically, `XCUITest` is used to write UI tests that interact with the application's UI elements, asserting that they exist, have the correct state, and respond appropriately to user interactions."
  },
  {
    "category": "General Frameworks & Tooling",
    "question": "Legacy JSON Frameworks: Can you name a JSON framework supported by iOS? (Referencing SBJson).",
    "answer": "The SBJson framework is a syntax analyzer and generator for Objective-C that handles JSON. It provides flexible APIs that simplify JSON handling. By using SBJson, developers can reduce the apparent latency of download/parse cycles over slow connections, begin parsing and returning chunks of documents asynchronously, and parse large documents bit by bit to conserve memory. (Note: While SBJson is historically relevant, modern Swift development typically utilizes the native Codable protocol or JSONSerialization.)"
  },
  {
    "category": "General Frameworks & Tooling",
    "question": "Linux/General Software Design: What is the use of design patterns in Linux?",
    "answer": "In Linux and general software design, design patterns provide reusable solutions to common problems. They establish a shared vocabulary for developers, improve code readability, architecture, and maintainability. In system programming, patterns like Singleton, Factory, and Observer are often implemented natively using specific system calls or file descriptors to manage shared resources and events."
  },
  {
    "category": "General Frameworks & Tooling",
    "question": "Algorithm Resources: References to open-source algorithm repositories like EKAlgorithm and swift-algorithm-club.",
    "answer": "For iOS developers, open-source algorithm repositories are valuable. `swift-algorithm-club` is a popular community-driven repository on GitHub that implements various algorithms and data structures in Swift with detailed explanations. `EKAlgorithm` is an older repository containing reusable algorithms and data structures for Objective-C."
  },
  {
    "category": "General Concepts & Methodology",
    "question": "What is waterfall methodology and Agile methodology? What are the differences between them?",
    "answer": "Waterfall methodology is a sequential model for software development. It is separated into a sequence of pre-defined phases including feasibility, planning, design, build, test, production, and support.\nOn the other hand, Agile development methodology is a linear sequential approach that provides flexibility for changing project requirements.\nList of differences:\nWaterfall model divides the software development process into different phases while Agile segregates the project development lifecycle into sprints. This makes waterfall more rigid while agile allows for more flexibility.\nWaterfall model describes the software development life cycle as a single project while Agile considers it as a collection of many different projects; iterations of different phases focus on improving overall software quality with feedback from users and the QA team.\nSince waterfall is more rigid, development requirements need to be clearly established beforehand since there is little flexibility for changing once project development starts. Meanwhile, Agile allows changes to be made anytime along the project development process even after initial planning has been completed.\nIn Waterfall, the testing phase typically occurs after the build phase. In Agile, testing is often performed concurrently with programming or at least in the same iteration.\nWaterfall is more of an internal process that does not involve user feedback. Agile tends to involve user participation more in order to improve customer satisfaction.\nWaterfall model best fits projects that have a clearly defined set of requirements and where a change to requirements is not expected. Agile fits more for projects where the requirements are expected to change and evolve.\nWaterfall can exhibit a project mindset that focuses on completion of the project while Agile can allow for more focus on developing a product that satisfies customers."
  },
  {
    "category": "General Concepts & Methodology",
    "question": "What is the difference between a class and an object?",
    "answer": "In the simplest sense, a class is a blueprint for an object. It describes the properties and behaviors common to any particular type of object. An object, on the other hand, is an instance of a class."
  },
  {
    "category": "General Concepts & Methodology",
    "question": "What is JSON? What are the pros and cons?",
    "answer": "JSON stands for JavaScript Object Notation. It is a file format that uses human-readable text to transmit data objects consisting of attribute-value pairs and array data types.\nPros: It is lighter than XML, meaning that it can represent the same data in XML in fewer bytes. This makes network transmissions and read/writes faster. Since it is native to JavaScript, computationally-expensive XSL transformations are not needed in order to extract data.\nCons: Not as widespread as XML. Data is not readily streamable and has to be broken up into individual objects. You can't use comments."
  },
  {
    "category": "General Concepts & Methodology",
    "question": "Can you name a JSON framework supported by iOS?",
    "answer": "The SBJson framework is a syntax analyzer and generator for Objective-C that handles JSON (JavaScript Object Notation), a lightweight data interchange format. It provides flexible APIs that simplify JSON handling. By using SBJson, developers can reduce the apparent latency of download/parse cycles over slow connections, begin parsing and returning chunks of documents asynchronously, and parse large documents bit by bit to conserve memory. (Note: While SBJson is historically relevant, modern Swift development typically utilizes the native Codable protocol or JSONSerialization.)"
  },
  {
    "category": "Design Patterns & Architecture",
    "question": "What is a Factory?",
    "answer": "As the name implies, it acts as a \"factory\" to generate instances of classes, and it is a creational design pattern. Here's how it works: If you have classes A, B, and C, you create a class X that acts as your factory. Inside class X, you have a function responsible for producing instances of A, B, and C. Most of the time, this is a static function so you don't need to create an instance of class X itself."
  },
  {
    "category": "Design Patterns & Architecture",
    "question": "What is an Observer?",
    "answer": "The Observer pattern is used when there is a one-to-many relationship between objects, such as if one object is modified, its dependent objects are notified automatically. The Observer pattern falls under the behavioral pattern category."
  },
  {
    "category": "Design Patterns & Architecture",
    "question": "What is a Coordinator?",
    "answer": "It acts like a tour guide in the application and is responsible for navigating between view controllers. While you could just use standard \"present\" or \"push\" transitions, using a coordinator reduces coupling between controllers by giving the coordinator the sole responsibility of handling navigation."
  },
  {
    "category": "Design Patterns & Architecture",
    "question": "What is a Proxy?",
    "answer": "In the proxy pattern, a class represents the functionality of another class. This falls under structural patterns. We create an object that holds the original object to interface its functionality to the outer world. It acts like a security guard holding the keys to various functions; it checks who has the authority to access a specific function in the class and grants access accordingly."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "What is Codable?",
    "answer": "Codable is a type alias that combines Encodable and Decodable. It is used to encode and decode custom data formats (like JSON and XML) to native Swift objects and vice versa."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "Do enums have strong or weak references in the memory?",
    "answer": "Enums do not have strong or weak references because they are value types. They generally pass a copy of the object rather than a reference to it."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "What is the first method that gets called in iOS?",
    "answer": "UIApplicationMain(_:_:_:_:) (and subsequently didFinishLaunchingWithOptions)."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "In an AppDelegate, how is the main UIWindow instantiated?",
    "answer": "If you choose the Storyboard option as you specify a template, the process works a little differently. The app is given a main storyboard, pointed to by the Info.plist key “Main storyboard file base name” (UIMainStoryboardFile).\nAfter UIApplicationMain instantiates the app delegate class, it asks the app delegate for the value of its window property; if that value is nil, the window is created and assigned to the app delegate’s window property. The storyboard’s initial view controller is then instantiated and assigned to the window’s rootViewController property, with the result that its view is placed in the window as its root view; the window is then sent the makeKeyAndVisible message. All of that is done behind the scenes by UIApplicationMain, with no visible code whatever. That is why, in a storyboard template, the application:didFinishLaunchingWithOptions: implementation is empty."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "Recursive enumeration",
    "answer": "A recursive enum is when an enumeration depends on itself (or another enum) as an associated value for one or more of its cases. We implement this by writing the indirect keyword before the specific case or before the enum declaration itself when creating it."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "List two types of classes in Swift.",
    "answer": "Subclass: It is the act of constructing a new class on an existing class. They inherit characteristics from the existing class, and you can further modify them with new characteristics.\nSuper Class: When a class inherits properties from another class, the inheriting class is known as a subclass, and the class it inherits from is called a superclass."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "Through which methods can you identify the layout of elements in UIView?",
    "answer": "Interface Builder: This provides developers with a visual collection of user interface objects and a drag-and-drop canvas to design layouts.\nNSLayoutConstraints: This defines the mathematical relationships between two user interface objects, which must be satisfied by the Auto Layout engine (the constraint-based layout system).\nCGRect: This is a structure that explicitly defines the location (x, y coordinates) and dimensions (width, height) of a rectangle for frame-based layouts."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "Define @synchronized?",
    "answer": "The @synchronized directive is a convenient way to create mutex locks on the fly in Objective-C code. The @synchronized directive does what any other mutex lock would do—it prevents different threads from acquiring the same lock at the same time."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "What is UIApplication and what does it really do?",
    "answer": "It is the heart of the iOS app and makes interaction easy between the system and other objects of the app."
  },
  {
    "category": "Swift & iOS Implementation",
    "question": "What are the biggest changes in UserNotifications?",
    "answer": "We can add audio, video, and images.\nWe can create custom interfaces for notifications.\nWe can manage notifications with interfaces in the notification center.\nNew Notification extensions allow us to manage remote notification payloads before they’re delivered."
  },
  {
    "category": "SwiftUI",
    "question": "Dedicated Definitions: Standalone, deep-dive explanations defining @State and @StateObject.",
    "answer": "`@State` is a property wrapper that allows a View to mutate and manage its own state internally; it is the source of truth for simple value types in SwiftUI and automatically redraws the view when changed. `@StateObject` is a property wrapper used to instantiate an `ObservableObject` type; unlike `@ObservedObject`, which might be recreated, `@StateObject` ensures the instance is created exactly once per view lifecycle, maintaining its data consistently across view updates."
  }
]

# Read README.md
with open('README.md', 'a') as f:
    f.write("\n\n## Additional Interview Questions\n\n")
    for q in data:
        f.write(f"### {q['question']} [Mid]\n\n")
        f.write(f"{q['answer']}\n\n---\n\n")

# Process index.html
with open('index.html', 'r') as f:
    html = f.read()

html_section = f"""
  <section class="cat-section" id="additional-interview-questions">
    <div class="category-header">
      <h2>Additional Interview Questions</h2>
      <span class="q-count">{len(data)} Questions</span>
    </div>
    <div class="accordion-list">
"""

for i, q in enumerate(data):
    html_section += f"""
    <div class="accordion-item" data-difficulty="mid" id="additional-interview-questions-q{i+1}">
      <button class="accordion-btn" aria-expanded="false" aria-controls="body-additional-interview-questions-q{i+1}">
        <span class="q-text">{q['question']}</span>
        <span class="btn-meta">
          <span class="badge badge-mid">Mid</span>
          <span class="chevron" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M5 7l4 4 4-4" stroke="currentColor" stroke-width="1.75"
                    stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </span>
      </button>
      <div class="accordion-body" id="body-additional-interview-questions-q{i+1}">
        <div class="accordion-inner"><p>{q['answer'].replace(chr(10), '<br/>')}</p></div>
      </div>
    </div>
"""

html_section += """
    </div>
  </section>
"""

# Insert right before </main>
insert_pos = html.find('  </main>')
if insert_pos != -1:
    new_html = html[:insert_pos] + html_section + html[insert_pos:]
    with open('index.html', 'w') as f:
        f.write(new_html)
else:
    print("Could not find </main> in index.html")

print("Done appending questions!")
