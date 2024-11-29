import enum


class ProfileType(str, enum.Enum):
    STUDENT = "student"
    SUPERVISOR = "supervisor"
    COSUPERVISOR = "cosupervisor"
    TEACHER_ASSISTANT = "teacher_assistant"
