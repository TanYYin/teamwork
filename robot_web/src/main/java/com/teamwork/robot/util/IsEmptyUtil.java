package com.teamwork.robot.util;

import com.teamwork.robot.model.node.Disease;
import com.teamwork.robot.result.Result;

import java.util.List;

/**
 * @author Xinjie
 * @date 2023/11/20 23:43
 */
public class IsEmptyUtil {

    public final static Result<Disease> NULL_Item= new Result<>(0, 204, "查询结果为空", null, 0L);
    public final static Result<Disease> FAIL_Item= new Result<>(1, 500, "参数为空格或格式错误");

   /* public final static Result<List<DiseaseResult>> NULL_Up= new Result<>(0, 204, "查询结果为空", null, 0L);
    public final static Result<List<DiseaseResult>> FAIL_Up= new Result<>(1, 500, "参数为空格或格式错误");
*/
/*    public static Result<List<NodesResult>> IsEmptyAndSize(List<NodesResult> list){
        try {
            //判断
            if(list==null || list.size()==0){
                return NULL;
            }else{
                return new Result<>(0, 200, "查询成功", list, (long) list.size());
            }
        } catch (Exception e) {
            e.printStackTrace();
            return FAIL;
        }
    }*/

    /**
     *
     * @param list 返回的list
     * @return 返回疾病信息
     */
    public static <T> Result<List<T>> IsEmptyAndSize(List<T> list){
        try {
            //判断
            if(list==null || list.size()==0){
                return new Result<>(0, 204, "查询结果为空", null, 0L);
            }else{
                return new Result<>(0, 200, "查询成功", list, (long) list.size());
            }
        } catch (Exception e) {
            e.printStackTrace();
            return new Result<>(1, 500, "参数为空格或格式错误");
        }
    }


   /* public static Result<List<DiseaseResult>> IsEmptyAndSizeUp(List<DiseaseResult> list){
        try {
            //判断
            if(list==null || list.size()==0){
                return NULL_Up;
            }else{
                return new Result<>(0, 200, "查询成功", list, (long) list.size());
            }
        } catch (Exception e) {
            e.printStackTrace();
            return FAIL_Up;
        }
    }*/

    /**
     *
     * @param disease disease
     * @return 返回的信息
     */
    public static Result<Disease> IsEmptyAndSizeItem(Disease disease){
        try {
            //判断
            if(disease==null||disease.getName()==null){
                return NULL_Item;
            }else{
                return new Result<>(0, 200, "查询成功", disease, 1L);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return FAIL_Item;
        }
    }
}
