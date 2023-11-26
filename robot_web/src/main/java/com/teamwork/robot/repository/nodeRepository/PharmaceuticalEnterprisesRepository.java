package com.teamwork.robot.repository.nodeRepository;

import com.teamwork.robot.model.node.PharmaceuticalEnterprises;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

/**
 * @author Crystry
 * @date 2021/11/22 21:42
 */
@Repository
public interface PharmaceuticalEnterprisesRepository extends Neo4jRepository<PharmaceuticalEnterprises,Long> {
}
