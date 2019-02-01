inherit extrausers

# set root password: titania
EXTRA_USERS_PARAMS += "usermod --password '\$6\$Sd9xDo1iCXoP4.h\$hnxuIsA3n2yZZ5GZH961ocjuaS44MWfdSntQFH8/6ddwP5Fb1xk8Y8IL/wrAT4.5Qtkty4QfV6Gh6i6lDvhC21' root;"
EXTRA_USERS_PARAMS += "groupadd --system wheel;"
EXTRA_USERS_PARAMS += "groupadd --non-unique --gid 65534 nobody;"
