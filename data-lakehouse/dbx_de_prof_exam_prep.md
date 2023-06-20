# dbx_de_prof_exam_prep

## Security

### Cluster access-control

- 2 types of permissions
  - allow cluster creation: admin controls who can create clusters 
  - cluster-level permission
    - view Spark UI, cluster metrics, driver logs -> min permission: Can Attach To
    - terminate, start, restart cluster -> min permission: Can Restart
    - Others -> min permission: Can Manage
 
    
    | Ability                                     | No Permissions | Can Attach To | Can Restart | Can Manage |
    |:---------------------------------------------|:----------------:|:---------------:|:-------------:|:------------:|
    | Attach notebook to cluster                  |                | x             | x           | x          |
    | View Spark UI, cluster metrics, driver logs |                | x             | x           | x          |
    | Terminate, start, restart cluster           |                |               | x           | x          |
    | Edit cluster                                |                |               |             | x          |
    | Attach library to cluster                   |                |               |             | x          |
    | Resize cluster                              |                |               |             | x          |
    | Modify permissions                          |                |               |             | x          |
