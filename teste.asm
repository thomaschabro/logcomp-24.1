PUSH DWORD 0 ;
MOV EAX, 1
MOV [EBP-4], EAX ;
LOOP_1:
MOV EAX, 5
PUSH EAX
MOV EAX, [EBP-4] ;
POP EBX
CMP EAX, EBX ;
SETL AL ;
MOVZX EAX, AL ;
CMP EAX, False
JE END_1
MOV EAX, 1
PUSH EAX
MOV EAX, [EBP-4] ;
POP EBX
ADD EAX, EBX ;
MOV [EBP-4], EAX ;
MOV EAX, [EBP-4] ;
PUSH EAX
PUSH formatout
CALL printf
ADD ESP, 8
JMP LOOP_1
END_1: