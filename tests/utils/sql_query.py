class Sql:
    @staticmethod
    def delete_user(phone, email):
        return 'DELETE FROM customers WHERE phone="{}" OR email="{}"'.format(phone, email)

    @staticmethod
    def delete_cart(data: dict):
        return f"DELETE FROM cart_temp WHERE id={data}"

    @staticmethod
    def get_order_ids(customer_id=20143):
        return f"SELECT id FROM `order` WHERE customer_id = {customer_id}"

    @staticmethod
    def get_usr_data(customer_id):
        return f"SELECT first_name, last_name, middle_name, email, phone FROM customers WHERE id = {customer_id}"

    @staticmethod
    def get_delivery_type_guid(type_name):
        return "SELECT guid FROM delivery_type WHERE name LIKE '{}'".format(type_name)

    @staticmethod
    def get_pick_up_addresses_guid():
        return 'SELECT name, guid FROM service_addresses'

    @staticmethod
    def get_order_by_order_id(order_id):
        return f'SELECT id FROM `order` WHERE id={order_id}'

