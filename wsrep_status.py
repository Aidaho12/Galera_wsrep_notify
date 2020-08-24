#!/usr/bin/python3
import os
import sys
import getopt
import socket

THIS_SERVER = socket.gethostname()

def telegram_send_mess(mess, **kwargs):
    import telebot
    from telebot import apihelper

    token_bot = ""
    channel_name = ""
    proxy = ""

    if proxy != 'None':
        apihelper.proxy = {'https': proxy}

    try:
        bot = telebot.TeleBot(token=token_bot)
        bot.send_message(chat_id=channel_name, text=mess)
    except Exception as e:
        print("Can't send message. Add Telegram channel before use alerting")
        print(e)
        pass


def main(argv):
    str_status = ''
    str_uuid = ''
    str_primary = ''
    str_members = ''
    str_index = ''
    message = ''

    usage = "Usage: " + os.path.basename(sys.argv[0]) + " --status <status str>"
    usage += " --uuid <state UUID> --primary <yes/no> --members <comma-seperated"
    usage += " list of the component member UUIDs> --index <n>"

    try:
        opts, args = getopt.getopt(argv, "h", ["status=","uuid=",'primary=','members=','index='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    if(len(opts) > 0):
        message_obj = GaleraStatus(THIS_SERVER)

        for opt, arg in opts:
            if opt == '-h':
                print(usage)
                sys.exit()
            elif opt in ("--status"):
                message_obj.set_status(arg)
            elif opt in ("--uuid"):
                message_obj.set_uuid(arg)
            elif opt in ("--primary"):
                message_obj.set_primary(arg)
            elif opt in ("--members"):
                message_obj.set_members(arg)
            elif opt in ("--index"):
                message_obj.set_index(arg)
        try:
            mes = 'Galera Notification: ' + THIS_SERVER + ' ' + str(message_obj)
            telegram_send_mess(mes)
        except Exception as e:
            print("Unable to send notification: %s" % e)
            sys.exit(1)
    else:
        print(usage)
        sys.exit(2)

    sys.exit(0)

class GaleraStatus:
    def __init__(self, server):
        self._server = server
        self._status = ""
        self._uuid = ""
        self._primary = ""
        self._members = ""
        self._index = ""
        self._count = 0

    def set_status(self, status):
        self._status = status
        self._count += 1

    def set_uuid(self, uuid):
        self._uuid = uuid
        self._count += 1

    def set_primary(self, primary):
        self._primary = primary.capitalize()
        self._count += 1

    def set_members(self, members):
        self._members = members.split(',')
        self._count += 1

    def set_index(self, index):
        self._index = index
        self._count += 1

    def __str__(self):
        message = "Galera running on " + self._server + " has reported the following"
        message += " cluster membership change"

        if(self._count > 1):
            message += "s"

        message += ":\n\n"

        if(self._status):
            message += "Status of this node: " + self._status + "\n\n"

        if(self._uuid):
            message += "Cluster state UUID: " + self._uuid + "\n\n"

        if(self._primary):
            message += "Current cluster component is primary: " + self._primary + "\n\n"

        if(self._members):
            message += "Current members of the component:\n"

            if(self._index):
                for i in range(len(self._members)):
                    if(i == int(self._index)):
                        message += "-> "
                    else:
                        message += "-- "

                    message += self._members[i] + "\n"
            else:
                message += "\n".join(("  " + str(x)) for x in self._members)

            message += "\n"

        if(self._index):
            message += "Index of this node in the member list: " + self._index + "\n"

        return message

if __name__ == "__main__":
    main(sys.argv[1:])
