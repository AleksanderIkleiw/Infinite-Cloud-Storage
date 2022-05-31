import pymongo
import dns.resolver


class MongoDb:
    def __init__(self, username='test'):
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = ['8.8.8.8']
        self.cluster = pymongo.MongoClient('mongodb string')
        self.database = self.cluster['CloudApp'][username]

    def insert_new_video_metadata(self, filename, length):
        self.database.insert_one({'_id': filename, 'length_of_the_file': int(length)})

    def get_size_of_the_file(self, filename):
        return self.database.find_one({'_id': filename})


if __name__ == '__main__':
    obj = MongoDb()
    obj.insert_new_video_metadata('test.mp3', '18')
    print(obj.get_size_of_the_file("big_file_to_convert.test"))
