from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb+srv://app:Password1@cluster0-yyeld.mongodb.net/test?retryWrites=true")


class DbClient:
    db = client["tradeit"]

    users = db['Users']
    products = db['Products']
    matches = db['Matches']

    def get_user_by_email(self, email):
        return self.users.find_one({'email': email})

    def get_user_by_id(self, user_id):
        return self.users.find_one({'_id': ObjectId(user_id)})

    def get_products(self):
        products = []
        for product in self.products.find():
            products.append(product)
        return products

    def add_product(self, user_id, product):
        product_id = self.products.insert_one(product).inserted_id
        self.users.update_one({'_id': ObjectId(user_id)}, {'$push': {'products': ObjectId(product_id)}})

    def remove_product(self, user_id, product_id):
        self.products.update_one({'_id': ObjectId(product_id)}, {'sale_state': 'Deleted'})
        self.users.update_one({'_id': ObjectId(user_id)}, {'$pull': {'products': ObjectId(product_id)}})

    def like_product(self, user_id, product_id):
        self.users.update_one({'_id': ObjectId(user_id)}, {'$push': {'likes': ObjectId(product_id)}})
        self.products.update_one({'_id': ObjectId(product_id)}, {'$push': {'liked': ObjectId(user_id)}})

    def dislike_product(self, user_id, product_id):
        self.users.update_one({'_id': ObjectId(user_id)}, {'$push': {'dislikes': ObjectId(product_id)}})

    def add_match(self, first_user, second_user, first_user_product_id, second_user_product_id):
        self.matches.insert(
            {'first_user_id': ObjectId(first_user), 'second_user_id': ObjectId(second_user),
             'first_user_product_id': ObjectId(first_user_product_id),
             'second_user_product_id': ObjectId(second_user_product_id)})

    def update_product_state(self, product_id, state):
        self.products.update_one({'_id': ObjectId(product_id)}, {'sale_state': state})

#
# if __name__ == '__main__':
#     db_client = DbClient()
#     db_client.get_user_by_id("5ca6607ab7635f3de065ad63")
#     db_client.add_match(first_user='5ca66093b7635f3de065ad64', first_user_product_id='5ca662d6b7635f3de065ad6a', second_user="5ca6607ab7635f3de065ad63", second_user_product_id="5ca66431b7635f3de065ad74")

# print(db_client.get_products())
# print(db_client.get_user_by_email('amiravrm@gmail.com'))
# print(db_client.get_user_by_id('5ca66093b7635f3de065ad64'))
# product = {'name': 'test'}
# db_client.add_product('5ca66093b7635f3de065ad64', product)
# db_client.like_product('5ca66093b7635f3de065ad64', '5ca662d6b7635f3de065ad6a')
# db_client.dislike_product('5ca66093b7635f3de065ad64', '5ca662d6b7635f3de065ad6a')
# db_client.add_match(first_user='5ca66093b7635f3de065ad64', first_user_product_id='5ca662d6b7635f3de065ad6a', second_user="5ca6607ab7635f3de065ad63", second_user_product_id="5ca66431b7635f3de065ad74")
