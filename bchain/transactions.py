from ecdsa import SigningKey


class Transaction:

    def __init__(self, t_type, passport_id, date_from, date_to, country, entity_id):
        self.t_type = t_type
        self.passport_id = passport_id 
        self.date_from = date_from
        self.date_to = date_to
        self.entity_id = entity_id

    def sign(self, private_key:SigningKey):
        self.signature = private_key.sign(self.string_to_sign)

    def string_to_sign(self):
        return (self.t_type +
                self.passport_id +
                self.date_from +
                self.date_to +
                self.entity_id)

    def to_string(self):
        return (self.t_type +
                self.passport_id +
                self.date_from +
                self.date_to +
                self.entity_id +
                self.signature)
    