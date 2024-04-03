## Database Schema

### Tables

| Table Name  | Description                            |
|-------------|----------------------------------------|
| Users       | Stores information about users.        |
| Items       | Stores information about products.      |
| Carts       | Stores information about user carts.   |
| CartItems   | Stores items in user carts.            |

### Relationships

- **Users to Carts:** One-to-many relationship. Each user can have multiple carts.
- **Carts to CartItems:** One-to-many relationship. Each cart can have multiple items.
- **Items to CartItems:** Many-to-one relationship. An item can be in multiple carts.

### Constraints

- **Users Table Constraints:**
  - Primary Key: user_id (unique identifier for users).
  - Other constraints as per business rules (e.g., unique username).

- **Items Table Constraints:**
  - Primary Key: item_id (unique identifier for items).
  - Price cannot be negative (Check constraint).

- **Carts Table Constraints:**
  - Primary Key: cart_id (unique identifier for carts).
  - Foreign Key: user_id (references user_id in Users table).

- **CartItems Table Constraints:**
  - Primary Key: cart_item_id (unique identifier for cart items).
  - Foreign Keys: cart_id (references cart_id in Carts table), item_id (references item_id in Items table).
