package com.hei.robot.repository.nodeRepository;

import com.hei.robot.model.node.Disease;
import org.springframework.data.neo4j.annotation.Query;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface DiseaseRepository extends Neo4jRepository<Disease,Long> {
    /**
     * 在疾病结点中属性查询 返回结点信息
     * @param name 疾病名称
     */
    @Query("Match (n:`疾病`) where n.name={name} return n")
    Disease findNodeByName(String name);


    /**
     * 在疾病结点中属性查询 返回结点信息
     * @param name 疾病名称
     */
    @Query("Match (n:`疾病`) where n.name={name} return n")
    List<Disease> findNodesByName(String name);

}
