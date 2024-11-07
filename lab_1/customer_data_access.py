from model_objects import Customer, ShoppingList, CustomerType, Address
from typing import List
import sqlite3


class CustomerMatches:
    def __init__(self):
        self.matchTerm = ""
        self.customer = None
        self.duplicates = []

    def has_duplicates(self) -> bool:
        """Check if there are duplicate customers."""
        return bool(self.duplicates)

    def add_duplicate(self, duplicate: Customer) -> None:
        """Add a duplicate customer to the list of duplicates."""
        self.duplicates.append(duplicate)


class CustomerDataAccess:
    def __init__(self, db: sqlite3.Connection):
        self.customerDataLayer = CustomerDataLayer(db)

    def load_company_customer(self, external_id: str, company_number: str) -> CustomerMatches:
        """
        Load a company customer by external ID or company number.
        
        :param external_id: External identifier for the customer.
        :param company_number: Unique company number.
        :return: CustomerMatches object containing matched customer and any duplicates.
        """
        matches = CustomerMatches()
        match_by_external_id = self.customerDataLayer.find_by_external_id(external_id)
        
        if match_by_external_id:
            matches.customer = match_by_external_id
            matches.matchTerm = "ExternalId"
            match_by_master_id = self.customerDataLayer.find_by_master_external_id(external_id)
            if match_by_master_id:
                matches.add_duplicate(match_by_master_id)
        else:
            match_by_company_number = self.customerDataLayer.find_by_company_number(company_number)
            if match_by_company_number:
                matches.customer = match_by_company_number
                matches.matchTerm = "CompanyNumber"

        return matches

    def load_person_customer(self, external_id: str) -> CustomerMatches:
        """
        Load an individual customer by external ID.
        
        :param external_id: External identifier for the customer.
        :return: CustomerMatches object containing matched customer.
        """
        matches = CustomerMatches()
        match_by_personal_number = self.customerDataLayer.find_by_external_id(external_id)
        matches.customer = match_by_personal_number
        if match_by_personal_number:
            matches.matchTerm = "ExternalId"
        return matches

    def update_customer_record(self, customer: Customer) -> None:
        """Update an existing customer record."""
        self.customerDataLayer.update_customer_record(customer)

    def create_customer_record(self, customer: Customer) -> Customer:
        """Create a new customer record."""
        return self.customerDataLayer.create_customer_record(customer)

    def update_shopping_list(self, customer: Customer, shopping_list: ShoppingList) -> None:
        """Add a shopping list to the customer and update the database."""
        customer.add_shopping_list(shopping_list)
        self.customerDataLayer.update_shopping_list(shopping_list)
        self.customerDataLayer.update_customer_record(customer)


class CustomerDataLayer:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def find_by_external_id(self, external_id: str) -> Customer:
        """
        Find a customer by external ID.
        
        :param external_id: External identifier for the customer.
        :return: Customer object if found, else None.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE externalId=?',
            (external_id,))
        return self.customer_from_sql_select_fields(self.cursor.fetchone())

    def find_address_id(self, customer: Customer) -> int:
        """
        Find the address ID for a given customer.
        
        :param customer: The customer whose address ID is to be found.
        :return: Address ID if found, else None.
        """
        self.cursor.execute('SELECT addressId FROM customers WHERE internalId=?', (customer.internalId,))
        result = self.cursor.fetchone()
        return int(result[0]) if result else 0

    def customer_from_sql_select_fields(self, fields: tuple) -> Customer:
        """
        Map SQL select fields to a Customer object.
        
        :param fields: Tuple of fields returned from a SQL query.
        :return: Customer object if fields are valid, else None.
        """
        if not fields:
            return None

        customer = Customer(
            internal_id=fields[0], external_id=fields[1], master_external_id=fields[2],
            name=fields[3], customer_type=CustomerType(fields[4]), company_number=fields[5]
        )
        
        address_id = self.find_address_id(customer)
        if address_id:
            self.cursor.execute('SELECT street, city, postalCode FROM addresses WHERE addressId=?', (address_id,))
            addresses = self.cursor.fetchone()
            if addresses:
                customer.address = Address(*addresses)

        self.cursor.execute('SELECT shoppinglistId FROM customer_shoppinglists WHERE customerId=?', (customer.internalId,))
        for (shopping_list_id,) in self.cursor.fetchall():
            self.cursor.execute('SELECT products FROM shoppinglists WHERE shoppinglistId=?', (shopping_list_id,))
            products = self.cursor.fetchone()[0].split(", ")
            customer.add_shopping_list(ShoppingList(products))
        return customer

    def find_by_master_external_id(self, master_external_id: str) -> Customer:
        """
        Find a customer by master external ID.
        
        :param master_external_id: Master external identifier for the customer.
        :return: Customer object if found, else None.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE masterExternalId=?',
            (master_external_id,))
        return self.customer_from_sql_select_fields(self.cursor.fetchone())

    def find_by_company_number(self, company_number: str) -> Customer:
        """
        Find a customer by company number.
        
        :param company_number: Unique company number.
        :return: Customer object if found, else None.
        """
        self.cursor.execute(
            'SELECT internalId, externalId, masterExternalId, name, customerType, companyNumber FROM customers WHERE companyNumber=?',
            (company_number,))
        return self.customer_from_sql_select_fields(self.cursor.fetchone())

    def create_customer_record(self, customer: Customer) -> Customer:
        """
        Create a new customer record in the database.
        
        :param customer: Customer object containing data for the new record.
        :return: The created Customer object.
        """
        customer.internalId = self.next_id("customers")
        self.cursor.execute(
            'INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?);',
            (customer.internalId, customer.externalId, customer.masterExternalId, customer.name,
             customer.customerType.value, customer.companyNumber, None)
        )
        
        if customer.address:
            address_id = self.next_id("addresses")
            self.cursor.execute(
                'INSERT INTO addresses VALUES (?, ?, ?, ?)',
                (address_id, customer.address.street, customer.address.city, customer.address.postalCode)
            )
            self.cursor.execute('UPDATE customers set addressId=? WHERE internalId=?', (address_id, customer.internalId))

        if customer.shoppingLists:
            for sl in customer.shoppingLists:
                data = ", ".join(sl)
                self.cursor.execute('SELECT shoppinglistId FROM shoppinglists WHERE products=?', (data,))
                shopping_list_id = self.cursor.fetchone()
                if not shopping_list_id:
                    shopping_list_id = self.next_id("shoppinglists")
                    self.cursor.execute('INSERT INTO shoppinglists VALUES (?, ?)', (shopping_list_id, data))
                self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)', (customer.internalId, shopping_list_id))

        self.conn.commit()
        return customer

    def next_id(self, table_name: str) -> int:
        """Generate the next unique ID for a specified table."""
        self.cursor.execute(f'SELECT MAX(ROWID) AS max_id FROM {table_name};')
        old_id = self.cursor.fetchone()[0]
        return int(old_id) + 1 if old_id else 1

    def update_customer_record(self, customer: Customer) -> None:
        """
        Update an existing customer record in the database.
        
        :param customer: Customer object containing updated data.
        """
        self.cursor.execute(
            'UPDATE customers SET externalId=?, masterExternalId=?, name=?, customerType=?, companyNumber=? WHERE internalId=?',
            (customer.externalId, customer.masterExternalId, customer.name, customer.customerType.value,
             customer.companyNumber, customer.internalId)
        )
        
        if customer.address:
            address_id = self.find_address_id(customer)
            if not address_id:
                address_id = self.next_id("addresses")
                self.cursor.execute(
                    'INSERT INTO addresses VALUES (?, ?, ?, ?)',
                    (address_id, customer.address.street, customer.address.city, customer.address.postalCode)
                )
                self.cursor.execute('UPDATE customers set addressId=? WHERE internalId=?', (address_id, customer.internalId))

        self.cursor.execute('DELETE FROM customer_shoppinglists WHERE customerId=?', (customer.internalId,))
        if customer.shoppingLists:
            for sl in customer.shoppingLists:
                products = ", ".join(sl.products)
                self.cursor.execute('SELECT shoppinglistId FROM shoppinglists WHERE products=?', (products,))
                shopping_list_ids = self.cursor.fetchone()
                if shopping_list_ids:
                    self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)', (customer.internalId, shopping_list_ids[0]))
                else:
                    shoppinglist_id = self.next_id("shoppinglists")
                    self.cursor.execute('INSERT INTO shoppinglists VALUES (?, ?)', (shoppinglist_id, products))
                    self.cursor.execute('INSERT INTO customer_shoppinglists VALUES (?, ?)',
                                        (customer.internalId, shoppinglist_id))

        self.conn.commit()

    def update_shopping_list(self, shopping_list):
        pass