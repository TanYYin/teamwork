package com.teamwork.robot.repository.relationshipRepo;

import com.teamwork.robot.model.relationship.DoEatRelationship;
import com.teamwork.robot.result.DiseaseResult;
import com.teamwork.robot.result.NodesResult;
import org.springframework.data.neo4j.annotation.Query;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * @author Crystry
 * @date 2021/11/23 16:04
 */
@Repository
public interface OtherRelationshipRepo extends Neo4jRepository<DoEatRelationship,Long> {

    @Query("MATCH (a:`疾病`)-[r]->(b) WHERE a.name={diseaseName} RETURN type(r) as type,b.name AS name")
    List<NodesResult> findLow(String diseaseName);


    @Query("MATCH (a:`疾病`)-[r]->(b) WHERE b.name={name} RETURN type(r) as type,a as disease")
    List<DiseaseResult> findDisease(String name);

    /*@Query("MATCH (a:`疾病`)-[r:do_eat]->(b:`食物`) WHERE a.name={diseaseName} RETURN b.name AS name")
    List<NodesResult> findFood(String diseaseName);

    @Query("MATCH (a:`疾病`)-[r:cure_department]->(b:`科室`) WHERE a.name={diseaseName} RETURN b.name AS name")
    List<NodesResult> findDepartment(String diseaseName);

    @Query("MATCH (a:`疾病`)-[r:has_common_drug]->(b:`药品`) WHERE a.name={diseaseName} RETURN b.name AS name")
    List<NodesResult> findDrugs(String diseaseName);

    @Query("MATCH (a:`疾病`)-[r:has_symptom]->(b:`症状`) WHERE a.name={diseaseName} RETURN b.name AS name")
    List<NodesResult> findSymptom(String diseaseName);

    @Query("MATCH (a:`疾病`)-[r:need_check]->(b:`检查`) WHERE a.name={diseaseName} RETURN b.name AS name")
    List<NodesResult> findCheck(String diseaseName);

    @Query("MATCH (a:`疾病`)-[r:not_eat]->(b:`食物`) WHERE a.name={diseaseName} RETURN b.name AS name")
    List<NodesResult> findNotEatFood(String diseaseName);

    @Query("MATCH (a:`疾病`)-[r:recommand_drug]->(b:`药品`) WHERE a.name={diseaseName} RETURN b.name AS name")
    List<NodesResult> findRecommendDrugs(String diseaseName);

    @Query("MATCH (a:`疾病`)-[r:recommand_recipes]->(b:`菜谱`) WHERE a.name={diseaseName} RETURN b.name AS name")
    List<NodesResult> findRecipes(String diseaseName);
*/
/*    @Query("MATCH (a:`疾病`)-[r]->(b) WHERE b.name={name} RETURN type(r) as type,a.name as name,a.prevent as prevent," +
            "a.get_prob as get_prob,a.symptom as symptom,a.cure_way as cure_way, a.cure_lasttime as cure_lasttime," +
            "a.cured_prob as cured_prob,a.cause as cause,a.cure_department as cure_department,a.easy_get as easy_get," +
            "a.desc as desc")*/
}

