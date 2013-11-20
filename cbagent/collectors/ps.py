from cbagent.collectors.libstats.psstats import PSStats
from cbagent.collectors import Collector


class PS(Collector):

    COLLECTOR = "atop"  # Legacy

    KNOWN_PROCESSES = ("beam.smp", "memcached", "sync_gateway")

    def __init__(self, settings):
        super(PS, self).__init__(settings)
        self.ssh_username = settings.ssh_username
        self.ssh_password = settings.ssh_password
        self.ps = PSStats(hosts=tuple(self.get_nodes()),
                          user=settings.ssh_username,
                          password=settings.ssh_password)

    def update_metadata(self):
        self.mc.add_cluster()
        for node in self.get_nodes():
            self.mc.add_server(node)

    def sample(self):
        for process in self.KNOWN_PROCESSES:
            for node, stats in self.ps.get_samples(process).items():
                if stats:
                    for title in stats:
                        self._update_metric_metadata(title, server=node)
                    self.store.append(stats,
                                      cluster=self.cluster, server=node,
                                      collector=self.COLLECTOR)