> All stuff is from Stanford CS142
# Webservers and Communication

- Browser<=>Webserver<=>Storage system
- low->high: IP->TCP->HTTP->REST
- DNS loop up->DNS res->HTTP req->HTTP res
## WebServers
- Browsers: send HTTP request and get HTTP responses
- Web Server: get HTTP requests and send HTTP responses

**HTTP is layered on TCP/IP so a web server:**
loop forever doing: accept TCP connection from browser=>read HTTP request from TCP connection=>process HTTP request=>write HTTP response to TCP connection=>shutdown TCP connection (except if Connection: keep-alive)

**Web server runs a program per request - the controller:**（后面有细节）

1. Parse URL and/or HTTP request body to get parameters to view
2. Use parameters to fetch **model** data from DBMS (typically a SQL relational DBMS)
3. Run HTML **view** template with model data to generate the HTML
4. Send a HTTP response with the HTML back to the browser

## Browser<=>webServer
###  HTTP: 
- HyperText Transfer Protocol
- Simple **request-response** protocol layered on TCP/IP (基本过程)
- Browser spends its life fetching things using HTTP: img, CSS, js, template, link 
#### request
Browser send HTTP request - write lines to socket(Method, URL, Protocal Version) 

1. Establish a **TCP/IP** connection to www.example.com:80
2. Send a http GET **request** along connection
3. Read from the connection the **response** from the web server

#### HTTP methods (重要)
- GET,HEAD,PUT,POST,DELETE
- **REST APIs** used GET, PUT, POST, and DELETE
	- 对应CRUD(Create, Read, Update, Delete) 

#### response
HTTP Response - Read lines from socket(Protocal Version, Status, Status message, body)  
200 OK, 400 Bad Request, 401 Unauthorized, 500 Internal Server Error, 404 Not Found

#### Caching Control
- (max-age=120 age out in 120 sec)
- Frequently used on fetches of static content like images, templates, CSS,JavaScript.
- Good: Reduce app startup latency and server load
- Bad: Changes might not be picked up right away(until the cache expires)
- When the browser sends a GET request, it receives a response in return. In the header of that response, the cache control property specifies how long that data lives in the cache.

## Controller/webServer Communication
- Browser is already talking to a web server, ask it for the model 
- Controller's job to fetch model for the view  

Feathers: 

- Allowed JavaScript to do a HTTP request without switching page
- Widely used and called **AJAX**： Asynchronous JavaScript and XML
- Since it is using an HTTP request it can carry XML or anything else

Approaches:

- Have the browser do a HTTP request for the model: **XMLHttpRequest**(``xhr.open(Method, URL);`` ``xhr.setRequestHeader();`` ``xhr.send();``)
	- Responses/errors come in as events
	- AJAX patterns: response in HTML or JS or Model Data(JSON)
- RESTful APIs and using AngularJS to access
- HTML5 WebSockets
- Remote PRocedure Call
- GraphQL

### REST APIs
- REST - representational state transfer
- Guidelines for web app to server communications

Attributes: 

- Server should export **resources** to clients using unique names (URIs)(e.g Photos, Users...)
- Keep servers "stateless" : 
	- 对单次请求的处理，不依赖其他请求，也就是说，处理一次请求所需的全部信息，要么都包含在这个请求里，要么可以从外部获取到（比如说数据库），服务器本身不存储任何信息 
	- Support easy load balancing across web servers
	- Allow caching of resources
- Server supports a set of HTTP methods mapping to **Create, Read, Update, Delete** (CRUD) on resource specified in the URL
	- **GET** method - Read resource (list on collection)(CSS, Controllers, templates, Model...)
	- **PUT** method - Update resource
	- **POST** method - Create resource (Model双向的)
	- **DELETE** method - Delete resource

**Angular accessing RESTful APIs**

- $http - Send an arbitrary HTTP request ($http.get, $http.post)(more general, lower level API)
- $resource - Interact with RESTful server-side data sources
	- Define a REST resource $resource ``var resource = $resource(resourceURL, parameters);``
	- Perform REST method on the resource  
	``resource.get(parameters, callback);``
	``resource.save(parameters, callback);``(query, delete as well)
	
e.g
	
	var PhotoListOfUser = $resource('/photos/:id', {id: '@id'}, {
			get: {method: 'get', isArray: true}
		});
	PhotoListOfUser.get({id: userId}, function(userPhotos) {
			console.log('userPhotos', userPhotos);
		});
	var AddComment = $resource('/commentsOfPhoto/:id', {id: photoId});
	AddComment.save({commentText: 'New Comment!'}, function (comment) {
			console.log('Added comment', comment);
		});
**Remote Procedure Call (RPC)**

- Traditional distributed computation technology supporting calling of a function on a remote machine.
- Allows arbitrary code to be run on server - handles complex, multiple resource operations(Reduces number of round trip messages and makes failure handling easier)
- Can result in more complex to use interface compared to REST(Need to document the API)
- RPC can be done over HTTP (e.g. POST) or WebSockets

**GraphQL**

- Server exports a "schema" describing the resources and supported queries.
- Client specifies what properties of the resource it is interested in retrieving.
- Can fetch from many different resources in the same request (i.e. entire model in one query).(快)
- Update operations specified in the exported schema(less info)
- Gives a program accessible backend(API)

# Node.js
- events
- fs
- async

## 特点
Javascript runs a **single-threaded** **event loop** that will handle events in **event queue**, and uses asynchronous calls to get around that, which means that if busy waiting is used in an event, it will halt the execution of all other events. 

- Take a JavaScript engine from a browser (Chrome's V8 JavaScript Engine)
	- Get same JavaScript on both browser and server
	- Don't need the DOM on the server
- Add **events and an event queue**
	- Everything runs as a call from the event loop (already had one for browser events)
- Make event interface to all OS operations
	- Wrap all the OS blocking calls (file and socket/network io)
	- Add some data handle support
- Add a proper module system
	- Each module gets its own scope (not everything in window)

###Event Queue：

- Inner loop: 每次pop出来一个event
- Never wait/block in event handler (或者写成callback的形式，参见fs example)
	1. launchReadRequest(socket); // Returns immediately
	2. When read finishes: eventQueue.push(readDoneEventHandler);
## How to use Node
### Node modules: 
- Import using ``require("fs") // system module; or from a file or directory`` (also has events, async)
- Module files have a private scope
	- Can declare variables that would be global in the browser
	- Require returns what is assigned to module.exports
- Standard Node Modules: fs, process acess, networking... (Huge lib of modules: **npm**)
	- **Express** and **Mongoose**(what we use)
### Node Buffer Class: (考)
- Manipulating lots of binary data wasn't a strength of the JavaScript engine
	- Unfortunately that is what web servers do: DBMS ⇔ Web Server ⇔ Browser
- Node add a Buffer class - **Optimized for storing and operating on binary data**
	- Interface looks an array of bytes (like the OS system calls use)
	- **Memory is allocated outside of the V8 heap**
- Used by the wrapped OS I/O calls (fs, net, …)
- Optimized **sharing with pointers** rather than always copying
	- buffer.copy()
	- For example: fs.readFile to socket.write

### Programming with Events/Callbacks
####Thread Programming VS. Events Programming(没考但感觉重要)
- Threads: Blocking/waiting is transparent
- Events: Blocking/waiting requires callback
 
If code doesn't block: Same as thread programming. If code does block (or needs to block): Need to setup callback; Often what was a return statement becomes a function call

#### step process example(重要)
Call **Pyramid of Doom** or **Callback Hell**
### Lister/Emitter pattern
- When **programing with events** (rather than threads) a listener/emitter pattern
is often used.
- **Listener** - Function to be called when the event is signaled. (Should be familiar from DOM programming (addEventListerner))
- **Emitter** - Signal that an event has occurred
	- Emit an event cause all the listener functions to be called
#### how to use
- ``EventEmitter = require('events');``

	    myEmitter.on('myEvent', function(param1, param2) {
	    		console.log('myEvent occurred with ' + param1 + ' and ' + param2 + '!');
	    	});// listen with on() and signal with emit()
	    myEmitter.emit('myEvent', 'arg1', 'arg2');
	    // listeners are called synchronously and in the order the listeners were registered
### Async Module (考)
Recall: Can't wait in NodeJS (总而言之都要写在括号里面)  
Write a function that turns waiting into a callback:  
``async.each()`` is a library function that will call another function on each of the elements of the array and wait for them to finish. Once all of them have finished it calls a second allDone function.  
``var async = require('async');``  
``async.each(list, func1, callback);// func1 干活，操作list``

## Stream 
### File I/O using stream 
- ``var readableStreamEvent = fs.createReadStream("smallFile");``  
``readableStreamEvent.on('data', function(){});``  
``readableStreamEvent.on('end', function(){});``  
``readableStreamEvent.on('error', function(){});``  
- ``var writableStreamEvent = fs.createWriteStream('outputFile');``
``writableStreamEvent.on('finish', function () {});``
``writableStreamEvent.write('Hello world!\n');``
``writableStreamEvent.end();``

## ExpressJS
### 特点
- A web framework for Node.js; Relatively thin layer on top of the base Node.js functionality
- expressApp object has methods for:
	- Routing HTTP requests
	- Rendering HTML (e.g. run a preprocessor like Jade templating engine)
	- Configuring middleware and preprocessorsvar 
- ``var express = require('express');``  

What a web server implementor need: 

- **Speak HTTP**: Accept TCP connections, process HTTP request, send HTTP replies; Node's HTTP module does this
- **Routing**: Map URLs to the web server function for that URL; Need to support a routing table (like ngRoute in AngularJS or React Router)
- **Middleware support**: Allow request processing layers to be added in; Make it easy to add custom support for sessions, cookies, security, compression, etc.

eg. 

    expressApp = express();
    expressApp.get('/', function (httpRequest, httpResponse) {
    	httpResponse.send('hello world');
    });
    expressApp.listen(3000);
    
    
expressApp object 
httpRequest object
httpResponse object

### How Express works
[Reference](https://www.jianshu.com/p/9333aa1b9320)  
[http://www.expressjs.com.cn/guide/routing.html](http://www.expressjs.com.cn/guide/routing.html)  

- [Routing](http://www.expressjs.com.cn/en/starter/basic-routing.html) 
- [Middleware](http://www.expressjs.com.cn/en/guide/using-middleware.html)
#### Express Routing
- expressApp object has HTTP methods: ``app.METHOD(PATH, HANDLER)`` 
	- METHOD is an HTTP request method, in lowercase.
	- PATH is a path on the server.
	- HANDLER is the function executed when the route is matched.(params: httpRequest, httpResponse)
- httpRequest object: man properties and can be added by Middleware
	- ``req.params/query/body/get()``
- httpResponse.object: setting HTTP response fields
	- ``res.write/status/send/write/end()``
#### Middleware (需要补充)
- Make it easy to add custom support for **sessions**, cookies, security, compression, etc.
- params: request obj, response obj, next middleware
- Make changes to the request and the response objects.
- End the request-response cycle.
- Call the next middleware function in the stack.
- Give other software the ability to interpose on requests
- ``app.all(urlPath, handler(req,res,next))`` on all request using the route 
- ``app.use(handler(req,res,next))``mechanismExecute any code.
- Example: 
	- Check to see if user is logged in, otherwise send error response and don't call next()
	- Parse the request body as JSON and attached the object to request.body and call next()
	- Session and cookie management, compression, encryption, etc.

**Give other software the ability to interpose on requests**

	 expressApp.all(urlPath, function (request, response, next) {
		 // Do whatever processing on request (or setting response)
	 	next(); // pass control to the next handler
	 });
**Interposing on all request using the route mechanism**
	
	expressApp.use(function (request, response, next) {...});

### Examples
**e.g Node nested callback**
	
	// impairs readability of the code
	fs.ReadFile(fileName, function (error, fileData) {
		doSomethingOnData(fileData, function (tempData1) {
			doSomethingMoreOnData(tempData1, function (tempData2) {
				finalizeData(tempData2, function (result) {
					doneCallback(result);
				});
			});
		});
	});

**e.g Fetching multiple models**

	app.get("/commentsOf/:objid", function (request, response) {
		var comments = [];
		fs.readFile("DB" + request.params.objid, function (error, contents) {
			var obj = JSON.parse(contents);
			async.each(obj.comments, fetchComments, allDone);
		});
		function fetchComments(commentFile, callback) {
			fs.readFile("DB"+ commentFile, function (error, contents) {
				if (!error) comments.push(JSON.parse(contents));
				callback(error);
			});
		}
		function allDone(error) {
			if (error) responses.status(500).send(error.message); else response.json(comments);
		}
	});

**eg. async.each() (超级重要)**

	async.each(array, function(elementInArray, callback) {
	    // Do something with elementInArray here.
	    // Call callback() or callback(err) when done
	    // - callback() (ie, without specifying a parameter) is used if what we did was successful
	    // callback(err) (ie, where we specify a parameter) is used if what we did was unsuccessful
	    }
	}, function(err) {
	    // Main callback -- async.each done processing at this point. Do something with the results here.  
	    // callback() was called on each element, then the main callback is invoked
	    // callback(err) was called on any element, then the main callback is immediately invoked immediately
	});

# Database
- Relational DB VS. noSQL DB
- How to use node module mongoose

## Relational DB
### Relational Database System
- Data is organized as a series of tables, a table is made of up of rows, a row is mad of a fixed (per table) set of typed columns
- Schema: The structure of the database
	- The table names (e.g. User, Photo, Comments)
	- The names and types of table columns
	- Various optional additional information (constraints, etc.)
- Structured Query Language (SQL): Queries is the strength of relational DB
- Using keys: primary key and secondary key
### Object Relational Mapping (ORM)
- mapping objects to SQL DB
- Rail's Active Record
	- Objects **map** to database records(**MongoDB doesn't have**)
	- One class for each table in the database (called Models in Rails)
	- Objects of the class correspond to rows in the table
	- Attributes of an object correspond to columns from the row
- Handled all the schema creation and SQL commands behind object interface

## NoSQL-MongoDB
### MongoDB - Most prominent NoSQL database
- Data model: Stores collections containing documents (JSON objects)
- Has expressive query language
- Can use indexes for fast lookups
- Tries to handle scalability, reliability, etc. 
### Schema enforcement
- JSON blobs provide super flexibility but not what is always wanted
	- Consider: \<h1>Hello {{person.informalName}}\</h1>
	- Good: typeof person.informalName == 'string' and length < something
	- Bad: Type is 1GB object, or undefined, or null, or …
- Would like to enforce a schema on the data
	- Can be implemented as validators on mutating operations
- Mongoose - Object Definition Language (ODL)
	- Take familiar usage from ORMs and map it onto MongoDB
	- Effectively masks the lower level interface to MongoDB with something that is friendlier 
## Using mongoose
### Mongoose - Object Definition Language (ODL)
- Mongoose maps ORM concepts to MongoDB
- Mongoose allows us to make schemas (can also refer to these as “models”) for more
structured queries to the DB
- Mongoose takes care of type casting and validation
- Any other correct explanation of something Mongoose improves, adds, or makes easier
### Procedure
- Connect to the MongoDB instance: ``mongoose.connect('mongodb://localhost/cs142');``
- Wait for connection to complete: Mongoose exports an EventEmitter: ``mongoose.connection.on('open', function () { // Can start processing model fetch requests});`` (can also listen to connecting/disconnecting/error...)
- Design Schema
- Make Model from Schema

### Mongoose Schema
Schema assign property names and their types to collections: 

- String, Number, Date, Buffer, Boolean
- Array - e.g. comments: [ObjectId]
- ObjectId - Reference to another object
- Mixed - Anything

eg. 

	var userSchema = new mongoose.Schema({
		user_id: String,
		emailAddresses: [String],
	});
### Secondary indexes (考)
- Performance and space trade-off
	- **Faster queries**: Eliminate scans - database just returns the matches from the index
	- **Slower** mutating operations: Add, delete, update must update indexes(update the index every time)
	- Uses more **space**: Need to store indexes and indexes can get bigger than the data itself
- When to use
	- Common queries spending a lot of time scanning
	- Need to **enforce uniqueness**
### Make Model from Schema
Like what each query does in SQL; A Model in Mongoose is a constructor of objects a collection May or may not correspond to a model of the MVC)

	var User = mongoose.model('User', userSchema);
	User.create({ first_name: 'Ian', last_name: 'Malcolm'}, doneCallback);
	function doneCallback(err, newUser) {
		assert (!err);
		console.log('Created object with ID', newUser._id);
	}
### Model used for query collection

	User.find(function (err, users) {/*users is an array of objects*/ }); // return a list; delete 也一样用
	User.findOne({_id: user_id}, function (err, user) { }); // return a single obj; delete 也一样用
	User.findOne({_id: user_id}, function (err, user) {
		// Update user object - (Note: Object is "special")
		user.save();
	}); // update a user obj
	
	var query = User.find({});
	query.select/sort/limit().exec(done_callback);

# Cookies and Sessions
## Session
In the **storage system**  
A session is a temporary and interactive information interchange between two or more communicating devices, or between a computer and user.

- Would like to **authenticate** user and have that information available each time
we process a request.
- More generally web apps would like to keep state per active browser - Called **session state**
- Look up problems and how to solve: HTTP request just come into a web server, need to include something in the request to tells us the session, using **cookies**; or using local storage API
## Cookie
- HTTP Cookie  
	- cookies are attached to **every HTTP request** sent from the browser to the website
	- respond: "Set-Cookies" in the header  
	- request: "Cookies" in the header
- Cookie content  
	- name and data: Domain for this cookie: server, port (optional), URL prefix (optional); The cookie is only included in requests matching its domain; Expiration date: browser can delete old cookies
	- Limits: Data size limited by browsers=># of cookies per server
## Session state and cookies
- store session state or pointers in cookies
- Place: web server's memory; storage system or specialize one

### ExpressJS dealing with session state  
- Stores a sessionID safely in a cookie
- Store session state in a session state store
- Like Rails, handles creation and fetching of session state for your request handlers

eg.

	var session = require('express-session')
	app.use(session({secret: 'badSecret'}));
		// secret is used to cryptographically sign the sessionID cookie
	app.get('/user/:user_id', function (httpRequest, httpResponse){}
		//httpRequest.session is an object you can read or write
### Web Storage API
- Cookie replacement
- **sessionStorage** :Per origin storage available when page is open; **localStorage**: Per origin storage with longer lifetime
- Standard key-value 
- Limited space (~10MB) and similar reliability issues to cookies

# Web App Security
## Outline
### Modes of attacks on web applications
- Attack the connection between browser and web server
○ Steal password
○ Hijack existing connection
- Attack the server
○ Inject code that does bad things
- Attack the browser
○ Inject code that does bad things
- Breach the browser, attack the client machine
- Fool the user (phishing) 

### Security Defences
- Isolation in browsers
- Cryptography
	- Protect information from unauthorized viewing
	- Detect changes
	- Determine origin of information
- Web development frameworks

#### Same-Origin Policy 
- One frame can **access** content in another frame only if they both came from the **same origin**(Protocal, Domain name, Port); Access applies to **DOM resource, cookies, XMLHttpRequest/AJAX requests**; **NO JS**; 
- There are times when it is useful for frames with different origins to communicate; (Limited to sub-domain sharing, font, Content distribution network)
- Browsers use the same-origin policy to restrict access to **cookies**.
#### Access-Control-Allow-Origin
- 解决跨域问题
- header in response: 要写允许的Origin, Method...
- ``postMessage(data, origin); window.addEventListener("message", callback); // callback 中检查origin``

## Network Attacks (考)
- **browser<=>server**
- use **encryption** to prevent eavesdropping and detect active attacks
- Each principal (user, program, etc.) has two encryption keys, one **public**, one **secret**(asymmetric)
	- Encrypt with public key: Only principle can access
	- Encrypt with secret key: Know that it comes from principle 
- **Certificate Authority**: find the public key for a particular server; well-known, trusted server that certifies public keys; **Certificate**: a document encrypted with the secret key of a certificate authority
	- Certificate authorities establish selfs as well known services on Internet(有很多CA)
	- Internet services compute keys, gives the public key to a certificate authority along with proof of identity; Certificate authority returns a certificate for that service
	- Service can pass along this certificate to browsers. Browser can validate the certificate came from the certification authority and see who the certification authority thinks the browser is talking to.
- **HTTPS**: SSL & TLS (可补充 HTTPS防了什么)
	- HTTP GET request: have the cookies including the **session cookie** attached allowing a "man-in-the-middle" attacker to steal and use to forge valid-looking requests to the backend.
	- Browser uses certificate to verify server's identity
	- Only one way: SSL/TLS does not allow the server to verify browser identity
	- Uses certificates and public-key encryption to pass a secret session-specific key from browser to server
- Problems of https
	- **SSL stripping**: When server returns pages with HTTPS links, attacker changes them to HTTP. When browser follows those links, attacker intercepts requests, creates its
	own HTTPS connection to server, and forwards requests via that.
	- **Mixed content**: Main page loaded with HTTPS, but some internal content loaded via HTTP(maybe developer error); Attackers can steal the session cookie from the HTTP GET request img. 
	- **"Just in time" HTTPS**: Login page displayed with HTTP; Before server returns HTML for login page, check for HTTPS; if page
	fetched via HTTP, redirect to the HTTPS version
	- Bad certificate

## Session Attacks
- Typically from cookies in the requset header; attacker can seal cookies
- **Session Hijacking**: attackers can impersonate you; 	
	- use cryptographically secure UID (not predictable)
	- use HTTPS; Change the session id after any change in privilege or security level
- **Browser quirk** involving cookies: (危险) Cookies sent with all HTTP requests to our web server; Other sites/apps running concurrently can generate HTTP requests to our web servers!
- **CSRF**: visit attacker's site with cookies of my real bank
	- even under one origin policy: Even under the same origin policy, HTTP requests generated by an attacker's HTML will have the cookies of the request destination attached by the browser. For backends that
use session cookies to authenticate requests these requests will look valid. Requests
can be generated by having an "a" tag that baits the user into clicking on it (GET
request) or by generating a form submit (GET or POST requests).
- **Data Tampering**: (Integrity)
	- Server sends information to browser (cookies, HTML with links & forms), but server can't trust what it gets back: User can view or modify anything provided by server; -Session information in cookies; -CSRF defence (hidden form fields)
	- Option #1: Server only uses information as a hint (must validate and correct): Means we have a store all the information on server
	- Option #2: Use cryptography to detect any tampering or forging: **Message Authentication Codes (MACs)**

### Message Authentication Codes (MACs) (考点)
- MAC function takes arbitrary-length text, secret key, produces a MAC that provides a **unique signature** for the text. Without knowing the **secret key**, cannot generate a valid MAC.
- **Browser<=>Server**: Server includes MAC with data sent to the browser.; Browser must return both MAC and data. Server can check the MAC using its secret key to detect tampering. Server checks input from browser and if MAC doesn't match tosses it (e.g. session cookie)
- MACs: **Authentication**, **Integrity**(Encryption: **Confidentiality**) (**重要**)

## Code Injection Attacks
### Code Injection on the Browser (考)
- Called a **Cross Site Scripting Attack** (XSS), Attacker stores attacking code in a victim Web server, where it gets accessed by victim clients; Consider following with a CSRF attack. JavaScript frameworks: Care is taken before stuffing things into the DOM
- **Reflected Cross Site Scripting Attack**: reflect attacks off the website or store on website
	- lure user to attacker site
	- attacker HTML automatically loads the link in an invisible iframe
	- AngularJS and React: **sanitize HTML**
### Code Injection on Server
- SQL injection: modify query to steal info or update db; dump the db
- Solutions: Don't use SQL; Use a framework that knows how to safely build sql commands (``routeParam.advisorName``)
## Phishing Attacks (需要补充)
- visit evil sites and disclose personal info
- Spoofing legitimate sites: img, look like(inl char)
- Problem: too easy to obtain certificates that look like legitimate sites; Solution: **extend validation**: CA 多审查 ; Browser provides special indicator for extended validation sites; Legitimate Web sites monitor traffic; Send emails
## Denial of Service Attacks (DOS Attacks)
- An attack that causes a service to fail by using up **resources**(/register, /login, /newPhoto ...)
- **Distributed Denial of Service** (DDoS) Attacks: DOS attack that uses many attacking machines
- Solution: resource quotas, raise resources cost,include a captcha before allowing the site to send resource-intensive API calls like fetching a user’s photos

## Conclusion
- Cross Site Request Forgery(CSRF)
	- We described two techniques for defeating CSRF. One invoked designing the backend web app to avoid HTTP verbs that an attacker could generate (GET and POST with arguments than can be generated via a form). The other was to have the backend generate a secret in the form that is passed to the frontend and checked on the backend 
- Cross Site Scripting Attack
	- The frontend code not allow user input to be injected into the DOM.
- SQL Injection
	- The backend should only generate proper SQL commands and not let SQL commands embedded in input data be executed.
- Phishing Attack
	- Mostly the frontend should provide some indication of where the page came from using HTTPS certificates.
- Denial Of Service Attack
	- The backend needs to protect itself from DoS attacks.

# Input and Validation
## Validation requirements in web applications
- Protect **integrity of storage** (required fields, organization, security, etc.)
	- Can not let HTTP request either from web app or generated out the web app damage us
	- Need to enforce at web server API
- Provide a good user experience
	- Don't let users make mistakes or warn them as soon as possible
	- Pushing validation closer to the user is helpful
- **Validation in JavaScript frameworks** (AngularJS/ReactJS)
	- ``required ng-minlength="3" ng-maxlength="20" ``
	- Rule #1: Still need server-side validation to protect storage system integrity
	- Rule #2: Let user know about validity problems as early as possible
	- Both frameworks followed familiar HTML form/input model
- **Server-side** validation
- Regardless of validation in browser server needs to check everything
	- Easy to directly access server API bypassing all browser validation checks
- Some integrity enforcement requires special code
	- Maintaining relationship between objects(Only author and admin user can delete a photo comment.)
	- Resource quotas(upload 50 photos unless they have a premium)

### Asynchronous validation
- Can in background communicate with web server to validate input
	- Example: username already taken
- Example: states search with **md-autocomplete**
	- ``<md-autocomplete md-selected-item="ctrl.selectedItem"
	 md-search-text="ctrl.searchText"
	 md-items="item in ctrl.querySearch(ctrl.searchText)"
	 md-item-text="item.display" placeholder="What is your favorite US state?">
	 <span md-highlight-text="ctrl.searchText">{{item.display}}</span>
	</md-autocomplete>``
- Trend towards using recommendation systems for input guidance

### React form input pattern - JSX
- Specifying a method as DOM event callback doesn't work:
``<form onSubmit={this.formSubmit}> … // Wrong! Calls with this undefined``
- Arrow function embedded in JSX render: Can call class method
``<form onSubmit={event -> this.formSubmit(event)}> …``
- Redefine method function in instance to have correct this in constructor:
``this.formSubmit = this.formSubmit.bind(this); // In component constructor``
### React input validation
- Unopinionated: meaning lots of unofficial options
	- Including some similar to the AngularJS support
- Roll your own. Example: Check inputs and set error message in state
``{ this.state.validationErrorMsg ?
 <span style={{color:'red'}}>
 {this.state.validationErrorMsg}
 </span>
 : null }``
- Style-guide driven classes are common. Example MaterializeCSS:
 ``<input className={!this.state.input1Invalid ? "invalid" : "valid"} ...``

### Single Page App Input
- Rather than POST with redirect you can do a XMLHttpRequest POST/PUT
- Angular supports two interfaces to XMLHttpRequest ($http and $resource)
``function FetchModel(url, doneCallback) {
$http.get(url).then(function(response) {
 var ok = (response.status === 200);
doneCallback(ok ? response.data : undefined);
 }, function(response) {
 doneCallback(undefined);
 });
}``

## Promises
- An alternative to pyramid: Have each callback be an individual function

### Idea behind promises 
- Rather than specifying a done callback
doSomething(args, doneCallback);
- Return a promise that will be filled in when done
var donePromise = doSomething(args);
donePromise will be filled in when operation completes
- Doesn't need to wait until you need the promise to be filled in
- Get the value of a promise (waiting if need be) with then

**Example of Promise usage**

	$http.get(url).then(function(response) {
	 			var ok = (response.status === 200);
				doneCallback(ok ? response.data : undefined);
	 		}, function(response) {
				doneCallback(undefined);
	 	}); // $http.get() returns a promise (as does axios)
 
**Converting callbacks to Promises**
	
	function myReadFile(filename) {
	 	return new Promise(function (fulfill, reject) {
	 		fs.readFile(filename, function (err, res) {
	 			if (err)
	 				reject(err);
	 			else
	 				fulfill(res);
	 		});
	 	});
	}

# Large-Scale Web Applications （还是有几个考点的）
## Scale-out
- **Scale-Out Architecture**(more instances: many servers, many storage systems)
- **Scale-up architecture** - Switch to a bigger instance

**Benefits of scale-out**

- Can scale to fit needs: Just add or remove instances
- Natural redundancy make tolerating failures easier: One instance dies others keep working

**Load-balancing switch**

- Special load balancer network switch
○ Incoming packets pass through load balancer switch between Internet and web servers
○ Load balancer directs TCP connection request to one of the many web servers
○ Load balancer will send all packets for that connection to the same server.
- In some cases the switches are smart enough to inspect session cookies, so
that the same session always goes to the same server.
- **Stateless servers** make load balancing easier (different requests from the
same user can be handled by different servers).
- Can select web server based on random or on load estimates

**nginx**

- Super efficient web server
- Shielding Node.js web servers
- Uses:
○ **Load balancing** - Forward requests to collection of front-end web servers
○ Handles front-end web servers coming and going (dynamic pools of server); Fault tolerant - web server dies the load balance just quits using it
○ Handles some simple request - static files, etc.
○ **DOS mitigation** - request rate limits

**Memcache** (考 可补充)

- Key-value store (both keys and values are arbitrary blobs)
- Used to cache results of recent database queries
- Much faster than databases: for **session state** requires fast access; tradeoff storing with lower reliability for lower resource consumption and higher speed

## Scale out web servers 
- Use **load balancing** to distribute incoming HTTP requests across many front-end web servers
	- **HTTP redirection**: Front-end machine accepts initial connections; Redirects them among an array of back-end machines
	-  **DNS** (Domain Name System) load balancing: Specify multiple targets for a given name; Handles geographically distributed system; DNS servers rotate among those targets
- **Scale-out assumption**(any web server will do)
	- **Stateless servers**: make load balancing easier: Different requests from the same user can be handled by different servers; Requires database to be shared across web servers
	- **Session state**: Accessed on every request so needs to be fast
	- **WebSockets** bind browsers and web server(can't load balance each request); Socket connection stays alive longer than a single request, which doesn’t work with load 
	- balancing.
- **Scale-out storage system**: Traditionally Web applications have started off using relational databases. A single database instance doesn't scale very far.
	- **Data sharding** - Spread database over scale-out instances: Each piece is called **data shard**; Can tolerate failures by **replication** - place more than one copy of data (3 is common)
	- Applications must partition data among multiple independent databases, which adds complexity.
- **Scale-out web architecture**: Internet--Load Balancer\*1--> webServers\*100-->Database Server\*50 + Memcache*20<--virtualization layer-->Physical Machines

## Cloud Computing (考)
- Idea: Use servers housed and managed by someone else (Use Internet to access them)
- **Virtualization** is a key enabler: Specify your compute, storage, communication needs:Cloud provider does the rest
- pay-for-resources-used
- Using scalable platform instead of managing virtual machines building skills
- Use cloud run databases
- **serveless**: Developer just specifies code to run on each URL & HTTP verb; Cloud provides services only (no servers)
	- In the serverless approach the developer doesn't view the cloud as a collection of servers but instead provides code that is run by a service being run by the cloud computing provider. Rather than viewing the backend as a collection of servers, the develop thinks in terms of events and functions to run when the events happen
	- Google Web Engine(**GAE**): good: Scale easily, Optimally configured security; bad: Inflexible, Hard to switch backend to something else later
- For webApps: pay-for-resources-used; useful infrastructure services; Cloud Application Programming Interfaces (APIs):

## Content Distribution Network (CDN)
- read-only part of our web app (e.g. image, html template, etc.), Browser needs to fetch but doesn't care where it comes from. **Only works on content that doesn't need to change often**
- **Content distribution network**: ○ Has many servers positions all over the world○ You give them some content (e.g. image) and they give you an URL○ You put that URL in your app (e.g. <img src="...)○ When user's browsers access that URL they are sent to the closest server (**DNS** trick: DNS servers will resolve the DNS query to IP addresses of different servers depending on the physical location of the browser running the web app)
- Benefits:○ Faster serving of app contents○ Reduce load on web app backend

