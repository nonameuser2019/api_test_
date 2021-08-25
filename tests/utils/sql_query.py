class Sql:
    @staticmethod
    def delete_user(phone, email):
        return 'DELETE FROM customers WHERE phone="{}" OR email="{}"'.format(phone, email)

    @staticmethod
    def delete_cart(data: dict):
        return f"DELETE FROM cart_temp WHERE id={data}"
