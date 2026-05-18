/*
 * SAL (Source Annotation Language) annotations are MSVC-only.
 * On other compilers (GCC/Clang) they are no-ops; define them here so the
 * MAPI headers compile without MSVC's sal.h providing them.
 */
#ifndef __in
#define __in
#endif
#ifndef __in_opt
#define __in_opt
#endif
#ifndef __out
#define __out
#endif
#ifndef __deref_out_ecount_full
#define __deref_out_ecount_full(x)
#endif
