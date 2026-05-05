# Playbook de refatoração

## 1. SQL concatenado para query parametrizada

Antes:

```python
cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
```

Depois:

```python
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## 2. Segredo embutido no código para settings

Antes:

```python
app.config["SECRET_KEY"] = "secret"
```

Depois:

```python
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
```

## 3. Lógica da rota para controller

Antes:

```javascript
app.post('/checkout', (req, res) => { /* validate, pay, persist */ });
```

Depois:

```javascript
router.post('/checkout', checkoutController.checkout);
```

## 4. God Class para módulos MVC

Antes:

```javascript
class AppManager { initDb() {} setupRoutes(app) {} checkout() {} report() {} }
```

Depois:

```text
config/ + models/ + services/ + controllers/ + routes/
```

## 5. Serialização repetida para método do model

Antes:

```python
data = {"id": task.id, "title": task.title}
```

Depois:

```python
data = task.to_dict()
```

## 6. Queries em loop para join/eager load

Antes:

```python
for task in tasks:
    user = User.query.get(task.user_id)
```

Depois:

```python
tasks = Task.query.options(joinedload(Task.user)).all()
```

## 7. Hash fraco para hash do framework

Antes:

```python
hashlib.md5(password.encode()).hexdigest()
```

Depois:

```python
generate_password_hash(password)
```

## 8. API obsoleta para API moderna

Antes:

```python
Task.query.get(task_id)
```

Depois:

```python
db.session.get(Task, task_id)
```

## 9. Endpoint admin inseguro para operação explícita

Antes:

```python
cursor.execute(request.json["sql"])
```

Depois:

```python
return jsonify({"error": "Disabled"}), 403
```

## 10. Callbacks aninhados para services

Antes:

```javascript
db.get(sql, params, () => db.run(sql2, params2, () => res.json(...)));
```

Depois:

```javascript
const result = await checkoutService.checkout(payload);
res.json(result);
```
