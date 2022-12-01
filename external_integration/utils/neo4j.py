from external_integration.constants import PROJECTS


def get_buildings(session, id_project, namespace, skip=0, limit=100):
    query = f"""MATCH (n:bigg__Building)-[:bigg__hasLocationInfo]-(l:bigg__LocationInfo),
                (l)-[:bigg__hasAddressCity]-(c), (n)-[]-(bs:bigg__BuildingSpace),
                 (bs)-[]-(d:bigg__Device),(d)-[:bigg__hasSensor]-(s)
                WHERE n.uri contains '{namespace}' AND c.geo__name='{PROJECTS[id_project]}'
                and s.bigg__timeSeriesEnd >= datetime('2021-12-01')
                RETURN n,l,c
                SKIP {skip}
                LIMIT {limit}"""
    return session.run(query)


def get_point_of_delivery(session, namespace, skip, limit):
    query = f"""MATCH (n:bigg__UtilityPointOfDelivery)-[r:bigg__hasUtilityType]-(u)
                WHERE n.uri contains "{namespace}"
                RETURN n.uri ,u.rdfs__label
                SKIP {skip}
                LIMIT {limit}
                """
    return session.run(query)


def get_sensors(session, id_project, namespace, skip, limit):
    query = f"""MATCH (lc)-[:bigg__hasAddressCity]-(l:bigg__LocationInfo)-[]-(b:bigg__Building)-[]-(bs:bigg__BuildingSpace)-[:bigg__isObservedByDevice]-(d)-[:bigg__hasSensor]-(s:bigg__Sensor)-[:bigg__hasMeasuredProperty]-(m)
                WHERE s.uri contains '{namespace}' and lc.geo__name='{PROJECTS[id_project]}' and s.bigg__timeSeriesEnd >= datetime('2021-12-01')
                RETURN s,m.uri
                SKIP {skip}
                LIMIT {limit}
            """
    return session.run(query)


def get_sensors_measurements(session, id_project, namespace, skip, limit):
    query = f"""MATCH (lc)-[:bigg__hasAddressCity]-(l:bigg__LocationInfo)-[]-(b:bigg__Building)-[]-(bs:bigg__BuildingSpace)-[:bigg__isObservedByDevice]-(d)-[:bigg__hasSensor]-(s:bigg__Sensor)-[:bigg__hasMeasurement]-(m:bigg__Measurement)
                WHERE s.uri contains '{namespace}' and lc.geo__name='{PROJECTS[id_project]}' and s.bigg__timeSeriesEnd >= datetime('2021-12-01')
                RETURN s,m
                SKIP {skip}
                LIMIT {limit}
            """

    return session.run(query)


def get_sensors_measurements_by_sensor_id(session, sensor_id, skip=0, limit=1000):
    query = f"""MATCH (lc)-[:bigg__hasAddressCity]-(l:bigg__LocationInfo)-[]-(b:bigg__Building)-[]-(bs:bigg__BuildingSpace)-[:bigg__isObservedByDevice]-(d)-[:bigg__hasSensor]-(s:bigg__Sensor)-[:bigg__hasMeasurement]-(m:bigg__Measurement)
                WHERE s.bigg__timeSeriesEnd >= datetime('2021-12-01') and s.uri contains '{sensor_id}'
                RETURN s,m
                SKIP {skip}
                LIMIT {limit}
            """

    return session.run(query)
