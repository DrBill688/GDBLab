IF EXIST "apache-tinkerpop-gremlin-server-3.7.3\bin\gremlin-server.bat" goto start_gremlin_server
curl https://dlcdn.apache.org/tinkerpop/3.7.3/apache-tinkerpop-gremlin-server-3.7.3-bin.zip --output apache-tinkerpop-gremlin-server-3.7.3-bin.zip
tar -xf apache-tinkerpop-gremlin-server-3.7.3-bin.zip
curl https://dlcdn.apache.org/tinkerpop/3.7.3/apache-tinkerpop-gremlin-console-3.7.3-bin.zip --output apache-tinkerpop-gremlin-console-3.7.3-bin.zip
tar -xf apache-tinkerpop-gremlin-console-3.7.3-bin.zip


:start_gremlin_server
echo "Starting Gremlin Server"
cd apache-tinkerpop-gremlin-server-3.7.3\bin
gremlin-server.bat

