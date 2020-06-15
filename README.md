# search_image

### /addImages

- #### methods

```
POST
```

- #### PARAM

| Param | Type | Description    | Examples                            |
| ----- | ---- | -------------- | ----------------------------------- |
| Id    | str  | image id array | news1,news2,news3                   |
| Image | str  | image array    | /data/1.png,/data/2.png,/data/3.png |



### /deleteImages

- #### methods

```
POST
```

- #### PARAM

| Param | Type | Description | Examples |
| ----- | ---- | ----------- | -------- |
| Id    | str  | image id    | news1    |



### /getSimilarImages

- #### methods


```
POST
```

- #### PARAM


| Param | Type | Description | Examples    |
| ----- | ---- | ----------- | ----------- |
| Id    | str  | image id    | news1       |
| Image | str  | image       | /data/1.png |



# Env

| Param            | Description                     | Defaults      |
| ---------------- | ------------------------------- | ------------- |
| MILVUS_HOST      | milvus container host           | 127.0.0.1     |
| MILVUS_PORT      | milvus container port           | 19530         |
| VECTOR_DIMENSION | default vector dimension number | 512           |
| METRIC_TYPE      | milvus metrics                  | MetricType.L2 |
| TOP_K            | num of the most similar vectors | 20            |
| DEFAULT_TABLE    | default milvus table            | milvus_image  |