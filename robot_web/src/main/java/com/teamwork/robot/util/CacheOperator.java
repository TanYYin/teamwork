package com.teamwork.robot.util;

import net.sf.json.JSONObject;

import java.io.*;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

/**
 * @author Xinjie
 * @date 2023/11/20 23:43
 */
public class CacheOperator {
    private CacheOperator(){}

    private static final String FILE_PATH = "D:\\code\\Software\\lala.json";

    private static class JsonHolder{
        private static Map<String,String> jsonMap;
        private static Map<String,String> latestMap;
        static {
            jsonMap = new HashMap<>();
            latestMap = new HashMap<>();
            loadJson(jsonMap);
        }
        //读取json文件进入内存
        private static void loadJson(Map<String,String> map){
            File file = new File(FILE_PATH);
            String s = "";
            try (InputStream inputStream = new FileInputStream(file)){
                byte[] bytes = new byte[1024*16];
                inputStream.read(bytes);
                s = new String(bytes);
            }catch (IOException e){
                e.printStackTrace();
            }
            defaultResolve(s,map);
        }

        //通过java依赖进行json的key-value解析
        private static void defaultResolve(String s,Map<String,String> map){
            //System.out.println(s);
            JSONObject jsonObject = JSONObject.fromObject(s);
            //System.out.println("---------------------");
            Iterator keys = jsonObject.keys();
            while (keys.hasNext()){
                String key = (String) keys.next();
                /*System.out.println("key:"+key);
                System.out.println("value:"+jsonObject.getString(key));
                System.out.println("----------------------");*/
                map.put(key,jsonObject.getString(key));
            }
        }
    }

    private static Map<String,String> getMap(){
        JsonHolder.jsonMap.clear();
        JsonHolder.loadJson(JsonHolder.jsonMap);
        return JsonHolder.jsonMap;
    }

    //将最新的json文件同步
    //会造成更新和删除失败的问题，暂时取消该功能，牺牲部分效率
    private static void LoadAndMerge(){
        JsonHolder.loadJson(JsonHolder.latestMap);
        JsonHolder.latestMap.putAll(JsonHolder.jsonMap);
        JsonHolder.jsonMap = null;
        JsonHolder.jsonMap = JsonHolder.latestMap;
    }


    public static boolean updateCache(String key,String value){
        Map<String,String> map = getMap();
        if(!map.containsKey(key)) return false;
        map.put(key,value);
        saveJson();
        return true;
    }

    public static boolean deleteCache(String key){
        Map<String,String> map = getMap();
        if(!map.containsKey(key)) return false;
        map.remove(key);
        saveJson();
        return true;
    }

    public static boolean addCache(String key,String value){
        getMap().put(key,value);
        saveJson();
        return true;
    }

    public static String showCache(){
        //不进行一致性操作了，管理员操作缓存期间的用户缓存更新将无效
        //LoadAndMerge();
        Map<String,String> map = JsonHolder.jsonMap;
        StringBuilder sb = new StringBuilder("{\n");
        for(String s:map.keySet()){
            String value = map.get(s);
            value=value.replaceAll("\n","\\\\n");
            sb.append("\t\"").append(s).append("\":");
            if(value.charAt(0)=='[' || value.charAt(0)=='{')
                sb.append(value).append(",\n");
            else sb.append("\""+value+"\"").append(",\n");
        }
        sb.deleteCharAt(sb.length()-2);
        sb.append("\n}");
        String res = new String(sb);
        return res;
    }

    private static void printMap(Map<String,String> map){
        for(String s:map.keySet()){
            System.out.println("key:"+s);
            System.out.println("value:"+map.get(s));
        }
    }

    //将修改后的json写入文件
    public static void saveJson(){
        String res = showCache();
        File f = new File(FILE_PATH);
        try (FileWriter fw = new FileWriter(f)){
            if(!f.exists()) f.createNewFile();
            fw.write(res);
        }catch (IOException e){
            e.printStackTrace();
        }
    }
}
