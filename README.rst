.. include:: replace.txt
.. highlight:: cpp

CISER Epidemic Routing
----------------

CISER Epidemic Routing protocol is a controlled flooding routing protocol
designed specifically for use in multi-hop wireless ad hoc networks
of mobile nodes. The work implemented based on the epidemiological
models of disease spread, specifically the CISER model as explained
in '[#Saha]_

The original SIR based model was developed by 
the `ResiliNets research group <http://www.ittc.ku.edu/resilinets>`_
at the University of Kansas.  

The CISER based model was developed by Ankush A. Mishra.

Installing
**********

To install these modules, you need to copy them into the top level directory
of ns-3, and then reconfigure your setup by::

  ./waf configure

followed by::

  ./waf

To use it, refer to the Helper Section.

Note: This was only tested on ns-3.27, and is not guaranteed to work on any other versions.

Routing Overview
*********************************

The implementation is based on the paper titled 'Epidemic Routing
for Partially-Connected Ad Hoc Networks.'[#Vahdat]_ while the added modes
are based on '[#Saha]_ , where we introduces two new states to the
original SIR Epidemic routing, called Carrier and Exposed state.


Useful parameters
=================

Epidemic routing supports these options:

  +----------------------+------------------------------------------+--------------+
  | Parameter            | Description                              |      Default |
  +----------------------+------------------------------------------+--------------+
  | HopCount             | Maximum number of hops a packet          |           64 |
  |                      | can be forwarded through.                |              |
  |                      | HopCount serves a similar                |              |
  |                      | function to TTL, but the 8-bit           |              |
  |                      | range of TTL is too small, so we         |              |
  |                      | use a 32-bit field as in                 |              |
  |                      | the paper.                               |              |
  +----------------------+------------------------------------------+--------------+
  | QueueLength          | Maximum number of packets that           |           64 |
  |                      | can be stored in Epidemic buffer         |              |
  +----------------------+------------------------------------------+--------------+
  | QueueEntryExpireTime | Maximum time a packet can live           |              |
  |                      | since generated at the source.           | Seconds(100) |
  |                      | Network-wide synchronization             |              |
  |                      | is assumed.                              |              |
  +----------------------+------------------------------------------+--------------+
  | HostRecentPeriod     | Time in seconds for host recent          |              |
  |                      | period, in which hosts can not           |  Seconds(10) |
  |                      | re-exchange summary vectors.             |              |
  +----------------------+------------------------------------------+--------------+
  | BeaconInterval       | Mean time interval between sending       |   Seconds(1) |
  |                      | beacon packets.                          |              |
  +----------------------+------------------------------------------+--------------+
  | BeaconRandomness     | Random number of milliseconds            |          100 |
  |                      | added at the beginning                   |              |
  |                      | of the BeaconInterval to avoid           |              |
  |                      | collisions.                              |              |
  +----------------------+------------------------------------------+--------------+
  | ExposedInterval      | The interval time for a node to start    |   Seconds(0) |
  |                      | sending packets to other nodes.          |              |
  +----------------------+------------------------------------------+--------------+
  | ExposedRandomness    | Upper bound of the uniform distribution  |          1.0 |
  |                      | random time for Exposed state.           |              |
  +----------------------+------------------------------------------+--------------+
  | CarrierProbability   | Probability of when a node upon          |          0.0 |
  |                      | receiving a message becomes a            |              |
  |                      | carrier node or not.                     |              |
  +----------------------+------------------------------------------+--------------+
  | CarrierRate          | Probability of the packets being         |              |
  |                      | sent if the node is a carrier.           |          1.0 |
  +----------------------+------------------------------------------+--------------+
  | CarrierInterval      | Time to reschedule the Carrier checking, |   Seconds(5) |
  |                      | and setting.                             |              |
  +----------------------+------------------------------------------+--------------+
  | CarrierRandomness    | Upper bound of the uniform distribution  |            1 |
  |                      | random time for Carrier checks.          |              |
  +----------------------+------------------------------------------+--------------+
  

Dropping Packets
================
Packets, stored in buffers, are dropped if they exceed HopCount, they are
older than QueueEntryExpireTime, or the holding buffer exceed QueueLength.  


Helper
******

To have a node run Epidemic Routing Protocol, the easiest way would be to use 
the EpidemicHelper
in your simulation script. For instance (assuming ``mainNodes`` 
is a ``NodeContainer``)::

  EpidemicHelper epidemic;
  mainNodes.Install (epidemic, adhocNodes);

This will run the epidemic routing using the default values. To use 
different parameter values::

  EpidemicHelper epidemic;
  epidemic.Set ("HopCount", UintegerValue (20));
  epidemic.Set ("QueueLength", UintegerValue (100));
  epidemic.Set ("QueueEntryExpireTime", TimeValue (Seconds (60)));
  epidemic.Set ("BeaconInterval", UintegerValue (5));
  mainNodes.Install (epidemic, adhocNodes);

Scripts
*******

Scripts to parallelize the execution and for multiple simulation
runs can be found in the scripts folder.

References
**********

.. rubric:: Footnotes

.. [#Vahdat] Amin Vahdat and David Becker, "Epidemic Routing for
   Partially-Connected Ad Hoc Networks," Duke University, Technical
   Report CS-200006, http://issg.cs.duke.edu/epidemic/epidemic.pdf
.. [#Saha] Hategekimana, Fidele, Snehanshu Saha, and Anita Chaturvedi.
   "Dynamics of Amoebiasis Transmission: Stability and
   Sensitivity Analysis." Mathematics 5.4 (2017): 58.,
   http://www.mdpi.com/2227-7390/5/4/58
