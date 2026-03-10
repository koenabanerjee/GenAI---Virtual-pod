# Software Design Specification for US-002: Mark tasks as completed in the todo app

## 1. Component Scope

The following components will be involved in implementing the "Mark tasks as completed" feature:

1. **Todo List Component**: This component will allow users to toggle the completion status of a task.
2. **Task Model**: The task model will store the completion status of each task.
3. **User Interface (UI)**: The UI will visually distinguish completed tasks from incomplete ones in the todo list.
4. **Reporting Component**: This component will allow users to view a report or filter of only completed tasks.

## 2. Architecture and Interfaces

The architecture of the system will follow a Model-View-ViewModel (MVVM) design pattern. The components will communicate with each other through well-defined interfaces.

### Interfaces

1. **ITodoListViewModel**: This interface will define methods for toggling the completion status of a task and retrieving a list of completed tasks.
2. **ITodoListView**: This interface will define methods for updating the UI when the completion status of a task changes and for displaying a report or filter of completed tasks.
3. **ITask**: This interface will define the contract for a task, including its completion status.

## 3. Data Contracts

### Task

```csharp
public class Task
{
    public int Id { get; set; }
    public string Title { get; set; }
    public bool IsCompleted { get; set; }
}
```

## 4. Risks and Mitigations

### Risk: Data inconsistency

Mitigation: Implement optimistic concurrency control to ensure that data remains consistent when multiple users attempt to mark the same task as completed.

## 5. Non-functional considerations

### Performance

To ensure good performance, consider implementing caching mechanisms to minimize database queries and reduce the load on the server. Additionally, consider implementing pagination or lazy loading to limit the amount of data that needs to be loaded at once.

### Security

Implement proper authentication and authorization mechanisms to ensure that only authorized users can mark tasks as completed and view completed task reports. Additionally, consider implementing input validation to prevent malicious users from manipulating the data.