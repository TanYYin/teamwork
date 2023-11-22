package com.teamwork.robot.repository.nodeRepository;

import com.teamwork.robot.model.node.Check;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/22/15:33
 * @Description:
 */
@Repository
public interface CheckRepository extends Neo4jRepository<Check,Long> {



}
