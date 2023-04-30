import pandas as pd
import networkx as nx 
import matplotlib.pyplot as plt

wireshark_url = '...Desktop/Network Analysis/datas.csv' #--->> CSV file directory

wireshark_data = pd.read_csv(wireshark_url)

sources = wireshark_data.groupby('Source').Source.count()
dest  = wireshark_data.groupby('Destination').Source.count()

wireshark_data['Protocol Count'] = wireshark_data.groupby('Protocol')['Protocol'].transform('count')

n = nx.from_pandas_edgelist(wireshark_data,source = 'Source',target = 'Destination',edge_attr = 'Protocol')

pos = nx.spring_layout(n,seed= 42)
nx.draw_networkx(n,pos,with_labels = True,node_size = 300)

dangerous_ips = sources[sources > 500].index.tolist()
dangerous_ips.extend(dest[dest>500].index.tolist())
options = {'node_size':1000,'node_color':'red'}
nx.draw_networkx_nodes(n,pos,nodelist=dangerous_ips,**options)



filtered_ips = [ip for ip in n.nodes() if not ip.startswith('192.168.1.129')] #---> optional
 
filtered_n = n.subgraph(filtered_ips)

pos_filtered  = nx.spring_layout(filtered_n,seed=42)


nx.draw_networkx(filtered_n,pos_filtered,with_labels =  True,node_size = 300)
filtered_dangerous_ips = [ip for ip in dangerous_ips if ip in filtered_n.nodes()]


options = {'node_size':1000,'node_color':'red'}

nx.draw_networkx_nodes(filtered_n,pos_filtered,nodelist = filtered_dangerous_ips,**options)

plt.show()

print('Done') #--->> check errors
