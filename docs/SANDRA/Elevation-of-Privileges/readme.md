---
layout: default
nav_order: 1
parent: SANDRA
title: SANDRA Elevation-of-Privileges
---
# SANDRA Elevation of Privileges via Arbitrary Physical Memory Mapping

## Summary

The AIDA Kernel Driver does not validate data received from the IRP->SystemBuffer.

Some IOCTL codes implement a logic where parameters arriving from the SystemBuffer 
are directly passed without validation to a routine that:
* Execute the `MmMapIoSpace` function which takes physical address, length, and cache type (hardcoded to 0) and maps specified physical memory into system memory.
* Execute `IoAllocateMdl` that uses the virtual address from `MmMapIoSpace` and the same Length value to associate the created MDL (Memory Descriptor List) with an IRP (I/O Request Packet).
* Then calls `MmBuildMdlForNonPagedPool`, that takes the newly created MDL and initialize the memory for the buffer.
* Finally, a call to `MmMapLockedPagesSpecifyCache`, which takes the allocated physical memory and maps it to a user-mode buffer.

Any user on the system can fully control the Physical Address and the size passed to the `MmMapIoSpace`,
and gets back the associated mapped user-mode address.

This technique can be successfully exploited using a physical memory "scanning" approach to find an elevated
process token ([Ruben Boonen][5] - IBM X-Force), egregiously explained by [h0mbre][4]

Affected by the vulnerability was the 0x22a428 IOCTL code. 

The weakness was discovered during February 2024.

## Vulnerable code

### IOCTL Dispatch

```
...
if (uVar5 < 0x22a429) {
  if (uVar5 == 0x22a428) {
    if ((_Dst != (ulonglong *)0x0) && (0x37 < uVar6)) {
      FUN_00011ab0(0x15110);
      puVar19 = &DAT_00015110;
LAB_000121fe:
      lVar17 = VulnerablePhysicalAllocation(_Dst,(longlong)puVar19);
      cVar9 = (char)lVar17;
LAB_00012206:
      bVar23 = cVar9 == '\0';
LAB_00012209:
      uVar15 = uVar21;
      if (!bVar23) goto LAB_0001231d;
LAB_00012c5c:
      uVar20 = uVar22;
      uVar15 = 0xc0000001;
      goto LAB_0001231d;
    }
  }
...
```

## Vulnerable Function

```c

longlong VulnerablePhysicalAllocation(PVOID buffer, PVOID outBuffer)

{
  ...
  VirtualAddress = MmMapIoSpace(
      *(UINT64*)buffer,*(UINT64*)((UINT64)buffer + 0x8), *(UINT64*)((UINT64)buffer + 0x14) == NULL)
      );
  *(PVOID *)(outBuffer + 0x28) = VirtualAddress;
  
  if (VirtualAddress != (PVOID)0x0) {
    if (*(UINT64*)((UINT64)buffer + 0x16) == NULL) {
      MemoryDescriptorList = IoAllocateMdl(
        VirtualAddress, *(DWORD*)((UINT64)buffer + 0x10), NULL, NULL, NULL
        );
      
      *(PMDL *)(outBuffer + 0x20) = MemoryDescriptorList;
      if (MemoryDescriptorList == (PMDL)0x0) {
        return 0;
      }
      
      MmBuildMdlForNonPagedPool(MemoryDescriptorList);
      
      VirtualAddress = MmMapLockedPagesSpecifyCache(
        *(PMDLX *)(outBuffer + 0x20),'\x01',
        (*(UINT64*)((UINT64)buffer + 0x14) == NULL),
        *(UINT64*)((UINT64)buffer + 0x8,
        0,
        NormalPagePriority
        );
      *(PVOID *)(outBuffer + 0x30) = VirtualAddress;
    }
   ...
   }
  return (longlong)VirtualAddress;
}
```

## Proof-of-Concept

It is possible for a low-privileged user in low integrity to elevate his privileges to NT System. 

## Remediation

No fix has been released or planned to be released for this bug. 

## References

* [Token Abuse for Privilege Escalation in Kernel][1]
* [Kernel Exploitation - _EPROCESS Hunt][3]
* [Kernel Exploitation - Kernel-2-User Mode Mapping Vulnerability][2]


[1]: https://www.ired.team/miscellaneous-reversing-forensics/windows-kernel-internals/how-kernel-exploits-abuse-tokens-for-privilege-escalation
[2]: https://h0mbre.github.io/atillk64_exploit/#
[3]: https://fuzzysecurity.com/tutorials/expDev/23.html
[4]: https://twitter.com/h0mbre_
[5]: https://twitter.com/FuzzySec