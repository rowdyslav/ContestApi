import dns.resolver
from environs import Env
from motor.motor_tornado import MotorClient

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
env = Env()
env.read_env()

client = MotorClient(env.str("MONGO_URL"))
db = client["ContestApi"]
