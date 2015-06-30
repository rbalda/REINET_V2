__author__ = 'rbalda'
from django.db import connection
from swampdragon.connections.sockjs_connection import DjangoSubscriberConnection
from swampdragon_auth.socketconnection import HttpDataConnection
from tornado import ioloop


class MysqlHeartbeatConnection(HttpDataConnection):
    def _close_db_connection(self):
        connection.close()

    def on_open(self, request):
        super(MysqlHeartbeatConnection, self).on_open(request)
        iol = ioloop.IOLoop.current()
        self.db_heartbeat = ioloop.PeriodicCallback(
            self._close_db_connection,
            callback_time=3000,
            io_loop=iol
        )
        self.db_heartbeat.start()

    def on_close(self):
        super(MysqlHeartbeatConnection, self).on_close()
        self._close_db_connection()
        self.db_heartbeat.stop()

    def on_message(self, data):
        self.db_heartbeat.stop()
        self.db_heartbeat.start()
        super(MysqlHeartbeatConnection, self).on_message(data)