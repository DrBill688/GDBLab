import logging, waitress, hupper, prometheus_flask_exporter, prometheus_client, werkzeug.middleware.dispatcher 
from flask import Flask


logging.basicConfig(format='<%(name)s> %(asctime)s %(filename)s:%(lineno)d:%(funcName)s => %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

TEMPLATE_PATH='templates'
DATA_PATH='c:\\Users\\wrone\\OneDrive\\FinDox\\FinDox.xlsm'
app = Flask('GDB Testing', template_folder=TEMPLATE_PATH)
app.secret_key='oh boy'
app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.DEBUG)
app.wsgi_app = werkzeug.middleware.dispatcher.DispatcherMiddleware(app.wsgi_app, {
    '/metrics': prometheus_client.make_wsgi_app()
})
metrics = prometheus_flask_exporter.PrometheusMetrics(app)
metrics.info('LocalFinance', 'DIM', version='0.0.1')

@app.route('/2')
def root2():
    from gremlin_python.process.anonymous_traversal import traversal
    from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
    rc = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    g = traversal().with_remote(rc)
    # retrieve the data from the "marko" vertex
    marko = g.V().has('person', 'name', 'marko').values('name').next()
    app.logger.error("name: " + marko)

    # find the "marko" vertex and then traverse to the people he "knows" and return their data
    people_marko_knows = g.V().has('person', 'name', 'marko').out('knows').values('name').to_list()
    for person in people_marko_knows:
        app.logger.error("marko knows " + person)
    rc.close()
    return "Hello2!"

@app.route('/')
def root():
    from gremlin_python.process.anonymous_traversal import traversal
    from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
    rc = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    g = traversal().with_remote(rc)
 # basic Gremlin: adding and retrieving data
    v1 = g.add_v('person').property('name', 'marko').next()
    v2 = g.add_v('person').property('name', 'stephen').next()
    v3 = g.add_v('person').property('name', 'vadas').next()

    # be sure to use a terminating step like next() or iterate() so that the traversal "executes"
    # iterate() does not return any data and is used to just generate side-effects (i.e. write data to the database)
    g.V(v1).add_e('knows').to(v2).property('weight', 0.75).iterate()
    g.V(v1).add_e('knows').to(v3).property('weight', 0.75).iterate()

    # retrieve the data from the "marko" vertex
    marko = g.V().has('person', 'name', 'marko').values('name').next()
    app.logger.error("name: " + marko)

    # find the "marko" vertex and then traverse to the people he "knows" and return their data
    people_marko_knows = g.V().has('person', 'name', 'marko').out('knows').values('name').to_list()
    for person in people_marko_knows:
        app.logger.error("marko knows " + person)

    rc.close()
    return "Hello!"
    
def run_server():
    app.logger.info('run_server()')
    host = 'localhost'
    port = 5002
    app.debug=True
    
    waitress.serve(app, host=host, port=port, threads=10)
    
if __name__ == '__main__':
    hupper.start_reloader('wsgi.run_server', ignore_files=[r'(.*)\.pyd'])
    
