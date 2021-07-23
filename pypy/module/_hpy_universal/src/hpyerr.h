#include "src/precommondefs.h"
#include "hpy.h"

RPY_EXTERN void pypy_HPy_FatalError(HPyContext *ctx, const char *message);
RPY_EXTERN int pypy_HPyErr_Occurred(HPyContext *ctx);
RPY_EXTERN void pypy_HPyErr_SetString(HPyContext *ctx, HPy type, const char *message);
RPY_EXTERN void pypy_HPyErr_SetObject(HPyContext *ctx, HPy type, HPy value);
RPY_EXTERN void pypy_HPyErr_Clear(HPyContext *ctx);
