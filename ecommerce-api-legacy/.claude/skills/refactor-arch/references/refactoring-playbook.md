# Refactoring Playbook

## 1. Concatenated SQL to Parameterized Query

Before:

```python
cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
```

After:

```python
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## 2. Hardcoded Secret to Settings

Before:

```python
app.config["SECRET_KEY"] = "secret"
```

After:

```python
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
```

## 3. Route Logic to Controller

Before:

```javascript
app.post('/checkout', (req, res) => { /* validate, pay, persist */ });
```

After:

```javascript
router.post('/checkout', checkoutController.checkout);
```

## 4. God Class to MVC Modules

Before:

```javascript
class AppManager { initDb() {} setupRoutes(app) {} checkout() {} report() {} }
```

After:

```text
config/ + models/ + services/ + controllers/ + routes/
```

## 5. Repeated Serialization to Model Method

Before:

```python
data = {"id": task.id, "title": task.title}
```

After:

```python
data = task.to_dict()
```

## 6. Queries in Loop to Join/Eager Load

Before:

```python
for task in tasks:
    user = User.query.get(task.user_id)
```

After:

```python
tasks = Task.query.options(joinedload(Task.user)).all()
```

## 7. Weak Hash to Framework Hash

Before:

```python
hashlib.md5(password.encode()).hexdigest()
```

After:

```python
generate_password_hash(password)
```

## 8. Deprecated API to Modern API

Before:

```python
Task.query.get(task_id)
```

After:

```python
db.session.get(Task, task_id)
```

## 9. Unsafe Admin Endpoint to Explicit Operation

Before:

```python
cursor.execute(request.json["sql"])
```

After:

```python
return jsonify({"error": "Disabled"}), 403
```

## 10. Nested Callbacks to Services

Before:

```javascript
db.get(sql, params, () => db.run(sql2, params2, () => res.json(...)));
```

After:

```javascript
const result = await checkoutService.checkout(payload);
res.json(result);
```
