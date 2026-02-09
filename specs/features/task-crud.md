# Feature Specification: Task CRUD Operations

## Overview

This specification defines the 5 Basic Level features for the Todo Console App:
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark as Complete

All features are accessed through a console menu interface.

---

## Feature 1: Add Task

### User Story
**As a user**, I can add a new task with a title and description, **so that** I can track things I need to do.

### Acceptance Criteria

#### AC1: Successful Task Creation
- **Given** the user selects "Add Task" from the menu
- **When** the user enters a valid title (1-200 characters)
- **And** optionally enters a description (max 1000 characters)
- **Then** a new task is created with:
  - Auto-generated unique ID
  - The provided title (trimmed of whitespace)
  - The provided description (trimmed of whitespace)
  - Completion status set to `False`
  - Current timestamp for `created_at`
  - Current timestamp for `updated_at`
- **And** a success message is displayed: "Task created successfully! (ID: {id})"
- **And** the user returns to the main menu

#### AC2: Empty Title Validation
- **Given** the user selects "Add Task"
- **When** the user enters an empty title or whitespace-only title
- **Then** an error message is displayed: "Error: Title cannot be empty"
- **And** the user is prompted to enter the title again
- **And** no task is created

#### AC3: Title Too Long Validation
- **Given** the user selects "Add Task"
- **When** the user enters a title longer than 200 characters
- **Then** an error message is displayed: "Error: Title cannot exceed 200 characters"
- **And** the user is prompted to enter the title again
- **And** no task is created

#### AC4: Description Too Long Validation
- **Given** the user has entered a valid title
- **When** the user enters a description longer than 1000 characters
- **Then** an error message is displayed: "Error: Description cannot exceed 1000 characters"
- **And** the user is prompted to enter the description again
- **And** no task is created

#### AC5: Empty Description Allowed
- **Given** the user has entered a valid title
- **When** the user presses Enter without typing a description
- **Then** the task is created with an empty description
- **And** the task is stored successfully

### Input Specifications

#### Title Input
- **Prompt**: "Enter task title: "
- **Type**: String
- **Required**: Yes
- **Validation**:
  - Must not be empty after stripping whitespace
  - Must not exceed 200 characters
- **Processing**: Strip leading/trailing whitespace before storage

#### Description Input
- **Prompt**: "Enter task description (optional, press Enter to skip): "
- **Type**: String
- **Required**: No
- **Validation**:
  - Must not exceed 1000 characters
- **Processing**: Strip leading/trailing whitespace before storage
- **Default**: Empty string if user presses Enter

### Output Specifications

#### Success Message
```
Task created successfully! (ID: 1)
```

#### Error Messages
```
Error: Title cannot be empty
Error: Title cannot exceed 200 characters
Error: Description cannot exceed 1000 characters
```

### Example Interaction

```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice: 1

Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread

Task created successfully! (ID: 1)

Press Enter to continue...
```

---

## Feature 2: View Task List

### User Story
**As a user**, I can view all my tasks with their details and status, **so that** I know what needs to be done.

### Acceptance Criteria

#### AC1: Display All Tasks
- **Given** there are tasks in the system
- **When** the user selects "View All Tasks"
- **Then** all tasks are displayed in order of creation (oldest first)
- **And** each task shows:
  - ID
  - Title
  - Description
  - Status (Pending or Completed)
  - Created timestamp
  - Updated timestamp
- **And** tasks are separated by a divider line
- **And** the user returns to the main menu after pressing Enter

#### AC2: Empty Task List
- **Given** there are no tasks in the system
- **When** the user selects "View All Tasks"
- **Then** a message is displayed: "No tasks found. Add a task to get started!"
- **And** the user returns to the main menu after pressing Enter

#### AC3: Task Status Display
- **Given** a task exists
- **When** the task is displayed
- **Then** the status shows:
  - "Pending" if `completed = False`
  - "Completed" if `completed = True`

#### AC4: Timestamp Formatting
- **Given** a task exists
- **When** the task is displayed
- **Then** timestamps are formatted as: "YYYY-MM-DD HH:MM:SS"
- **Example**: "2025-12-05 14:30:00"

### Output Specifications

#### Task Display Format
```
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending
Created: 2025-12-05 10:30:00
Updated: 2025-12-05 10:30:00
---
ID: 2
Title: Call mom
Description: 
Status: Completed
Created: 2025-12-05 09:15:00
Updated: 2025-12-05 14:20:00
---
```

#### Empty List Message
```
No tasks found. Add a task to get started!
```

### Example Interaction

```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice: 2

=== All Tasks ===

ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending
Created: 2025-12-05 10:30:00
Updated: 2025-12-05 10:30:00
---
ID: 2
Title: Call mom
Description: 
Status: Completed
Created: 2025-12-05 09:15:00
Updated: 2025-12-05 14:20:00
---

Press Enter to continue...
```

---

## Feature 3: Update Task

### User Story
**As a user**, I can update a task's title and description, **so that** I can correct or clarify information.

### Acceptance Criteria

#### AC1: Successful Task Update
- **Given** the user selects "Update Task"
- **When** the user enters a valid task ID
- **And** the task exists
- **And** the user enters a new valid title
- **And** the user enters a new description (or skips)
- **Then** the task is updated with:
  - The new title (trimmed)
  - The new description (trimmed)
  - `updated_at` set to current timestamp
  - `completed` status unchanged
  - `created_at` unchanged
  - `id` unchanged
- **And** a success message is displayed: "Task {id} updated successfully!"
- **And** the user returns to the main menu

#### AC2: Task Not Found
- **Given** the user selects "Update Task"
- **When** the user enters a task ID that doesn't exist
- **Then** an error message is displayed: "Error: Task {id} not found"
- **And** the user returns to the main menu
- **And** no changes are made

#### AC3: Invalid Task ID Input
- **Given** the user selects "Update Task"
- **When** the user enters a non-numeric value
- **Then** an error message is displayed: "Error: Please enter a valid task ID (number)"
- **And** the user is prompted to enter the ID again

#### AC4: Title Validation on Update
- **Given** the user is updating a task
- **When** the user enters an empty or whitespace-only title
- **Then** an error message is displayed: "Error: Title cannot be empty"
- **And** the user is prompted to enter the title again
- **And** the task is not updated

#### AC5: Show Current Values
- **Given** the user enters a valid task ID
- **When** the update prompts are displayed
- **Then** the current title and description are shown
- **And** the user can see what they're updating

### Input Specifications

#### Task ID Input
- **Prompt**: "Enter task ID to update: "
- **Type**: Integer
- **Required**: Yes
- **Validation**: Must be a valid integer

#### Title Input
- **Prompt**: "Enter new title (current: {current_title}): "
- **Type**: String
- **Required**: Yes
- **Validation**: Same as Add Task

#### Description Input
- **Prompt**: "Enter new description (current: {current_description}, press Enter to keep): "
- **Type**: String
- **Required**: No
- **Validation**: Same as Add Task

### Output Specifications

#### Success Message
```
Task 1 updated successfully!
```

#### Error Messages
```
Error: Task 5 not found
Error: Please enter a valid task ID (number)
Error: Title cannot be empty
Error: Title cannot exceed 200 characters
Error: Description cannot exceed 1000 characters
```

### Example Interaction

```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice: 3

Enter task ID to update: 1

Current Task:
Title: Buy groceries
Description: Milk, eggs, bread

Enter new title: Buy groceries and fruits
Enter new description (press Enter to keep current): Milk, eggs, bread, apples, oranges

Task 1 updated successfully!

Press Enter to continue...
```

---

## Feature 4: Delete Task

### User Story
**As a user**, I can delete a task, **so that** I can remove completed or cancelled items.

### Acceptance Criteria

#### AC1: Successful Task Deletion
- **Given** the user selects "Delete Task"
- **When** the user enters a valid task ID
- **And** the task exists
- **And** the user confirms deletion
- **Then** the task is permanently removed from storage
- **And** a success message is displayed: "Task {id} deleted successfully!"
- **And** the user returns to the main menu

#### AC2: Task Not Found
- **Given** the user selects "Delete Task"
- **When** the user enters a task ID that doesn't exist
- **Then** an error message is displayed: "Error: Task {id} not found"
- **And** the user returns to the main menu
- **And** no changes are made

#### AC3: Deletion Confirmation
- **Given** the user enters a valid task ID
- **When** the task is found
- **Then** the task details are displayed
- **And** a confirmation prompt is shown: "Are you sure you want to delete this task? (y/n): "
- **And** deletion only proceeds if user enters 'y' or 'Y'

#### AC4: Deletion Cancelled
- **Given** the user is prompted to confirm deletion
- **When** the user enters 'n', 'N', or any other value
- **Then** a message is displayed: "Deletion cancelled"
- **And** the task is not deleted
- **And** the user returns to the main menu

#### AC5: Invalid Task ID Input
- **Given** the user selects "Delete Task"
- **When** the user enters a non-numeric value
- **Then** an error message is displayed: "Error: Please enter a valid task ID (number)"
- **And** the user is prompted to enter the ID again

### Input Specifications

#### Task ID Input
- **Prompt**: "Enter task ID to delete: "
- **Type**: Integer
- **Required**: Yes
- **Validation**: Must be a valid integer

#### Confirmation Input
- **Prompt**: "Are you sure you want to delete this task? (y/n): "
- **Type**: String
- **Required**: Yes
- **Valid Values**: 'y', 'Y', 'n', 'N', or any other (treated as 'n')

### Output Specifications

#### Success Message
```
Task 1 deleted successfully!
```

#### Cancellation Message
```
Deletion cancelled.
```

#### Error Messages
```
Error: Task 5 not found
Error: Please enter a valid task ID (number)
```

### Example Interaction

```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice: 4

Enter task ID to delete: 1

Task to delete:
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending

Are you sure you want to delete this task? (y/n): y

Task 1 deleted successfully!

Press Enter to continue...
```

---

## Feature 5: Mark Task Complete/Incomplete

### User Story
**As a user**, I can mark a task as complete or incomplete, **so that** I can track my progress.

### Acceptance Criteria

#### AC1: Toggle to Completed
- **Given** the user selects "Mark Task Complete/Incomplete"
- **When** the user enters a valid task ID
- **And** the task exists with `completed = False`
- **Then** the task's `completed` status is set to `True`
- **And** the `updated_at` timestamp is updated
- **And** a success message is displayed: "Task {id} marked as completed!"
- **And** the user returns to the main menu

#### AC2: Toggle to Incomplete
- **Given** the user selects "Mark Task Complete/Incomplete"
- **When** the user enters a valid task ID
- **And** the task exists with `completed = True`
- **Then** the task's `completed` status is set to `False`
- **And** the `updated_at` timestamp is updated
- **And** a success message is displayed: "Task {id} marked as incomplete!"
- **And** the user returns to the main menu

#### AC3: Task Not Found
- **Given** the user selects "Mark Task Complete/Incomplete"
- **When** the user enters a task ID that doesn't exist
- **Then** an error message is displayed: "Error: Task {id} not found"
- **And** the user returns to the main menu
- **And** no changes are made

#### AC4: Invalid Task ID Input
- **Given** the user selects "Mark Task Complete/Incomplete"
- **When** the user enters a non-numeric value
- **Then** an error message is displayed: "Error: Please enter a valid task ID (number)"
- **And** the user is prompted to enter the ID again

#### AC5: Show Current Status
- **Given** the user enters a valid task ID
- **When** the task is found
- **Then** the current status is displayed before toggling
- **And** the user can see the status change

### Input Specifications

#### Task ID Input
- **Prompt**: "Enter task ID to toggle completion: "
- **Type**: Integer
- **Required**: Yes
- **Validation**: Must be a valid integer

### Output Specifications

#### Success Messages
```
Task 1 marked as completed!
Task 1 marked as incomplete!
```

#### Error Messages
```
Error: Task 5 not found
Error: Please enter a valid task ID (number)
```

### Example Interaction

```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice: 5

Enter task ID to toggle completion: 1

Current Status: Pending

Task 1 marked as completed!

Press Enter to continue...
```

---

## Console Menu Specification

### Main Menu Display

```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice: 
```

### Menu Behavior

#### Valid Choice
- **Given** the user enters a number 1-6
- **When** the choice is processed
- **Then** the corresponding feature is executed
- **And** the user returns to the menu after completion (except Exit)

#### Invalid Choice
- **Given** the user enters an invalid value (not 1-6)
- **When** the choice is processed
- **Then** an error message is displayed: "Invalid choice. Please enter a number between 1 and 6."
- **And** the menu is displayed again

#### Exit Choice
- **Given** the user enters "6"
- **When** the choice is processed
- **Then** a goodbye message is displayed: "Thank you for using Todo App. Goodbye!"
- **And** the application exits cleanly

---

## Error Handling Summary

| Error Type | Message | Recovery |
|------------|---------|----------|
| Empty title | "Error: Title cannot be empty" | Re-prompt for title |
| Title too long | "Error: Title cannot exceed 200 characters" | Re-prompt for title |
| Description too long | "Error: Description cannot exceed 1000 characters" | Re-prompt for description |
| Task not found | "Error: Task {id} not found" | Return to menu |
| Invalid task ID | "Error: Please enter a valid task ID (number)" | Re-prompt for ID |
| Invalid menu choice | "Invalid choice. Please enter a number between 1 and 6." | Show menu again |

---

## Non-Functional Requirements

### Performance
- All operations must complete in < 100ms
- Menu display must be instant

### Usability
- Clear prompts for all inputs
- Helpful error messages
- Consistent formatting
- Easy navigation

### Reliability
- No crashes on invalid input
- Graceful error handling
- Data integrity maintained

---

## Testing Scenarios

### Happy Path
1. Add 3 tasks with various titles and descriptions
2. View all tasks
3. Update task 2
4. Mark task 1 as complete
5. View all tasks (verify update and completion)
6. Delete task 3
7. View all tasks (verify deletion)
8. Exit

### Edge Cases
1. Add task with empty title (should fail)
2. Add task with 200-character title (should succeed)
3. Add task with 201-character title (should fail)
4. Update non-existent task (should fail)
5. Delete non-existent task (should fail)
6. Toggle completion on non-existent task (should fail)
7. View tasks when list is empty
8. Add task with empty description (should succeed)

### Error Recovery
1. Enter invalid menu choice (verify recovery)
2. Enter non-numeric task ID (verify recovery)
3. Cancel deletion (verify task remains)
4. Enter invalid title, then valid title (verify retry works)

---

## Compliance Checklist

- ✅ All 5 features specified
- ✅ User stories defined
- ✅ Acceptance criteria complete
- ✅ Input specifications detailed
- ✅ Output specifications defined
- ✅ Error handling specified
- ✅ Example interactions provided
- ✅ Testing scenarios outlined
