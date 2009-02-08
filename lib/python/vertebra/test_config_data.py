GLOBAL_POLICY = { # All apps aren't in debug mode
  'admin': 'res:/',
  'debug': 'bool:false',
  'top': 'str:global',
}

COMPANY_POLICY = { # Engine Yard's System Apps are in debug mode
  'admin': 'res:/engineyard',
  'app': 'res:/sys',
  'debug': 'bool:true',
  'top': 'str:company',
}

APP_POLICY = { # System VM App Default
  'app': 'res:/sys/vm',
  'debug': 'bool:false',
  'top': 'str:app',
}

CLUSTER_POLICY = { # Policies for all Clusters
  'admin': 'res:/engineyard',
  'logserver': 'blah@blah.blah',
}

CLUSTER5_POLICY = { #  Policy for Cluster 5
  'admin': 'res:/engineyard',
  'cluster': 'res:/cluster/5',
  'debug': 'bool:false',
  'top': 'str:c5',
}

US_POLICY = { # Policy for US
  'where': 'res:/earth/us',
  'top': 'str:us',
}


