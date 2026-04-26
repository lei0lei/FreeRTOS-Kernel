# lib_AT91SAM7X128.h 代码解说

源文件：`portable/IAR/AtmelSAM7S64/lib_AT91SAM7X128.h`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 预处理配置 AT91F_AIC_ConfigureIt

```c
/** ---------------------------------------------------------------------------- */
/**         ATMEL Microcontroller Software Support  -  ROUSSET  - */
/** ---------------------------------------------------------------------------- */
/** DISCLAIMER:  THIS SOFTWARE IS PROVIDED BY ATMEL "AS IS" AND ANY EXPRESS OR */
/** IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF */
/** MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT ARE */
/** DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR ANY DIRECT, INDIRECT, */
/** INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT */
/** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, */
/** OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF */
/** LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING */
/** NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, */
/** EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. */
/** ---------------------------------------------------------------------------- */
/** File Name           : lib_AT91SAM7X128.h */
/** Object              : AT91SAM7X128 inlined functions */
/** Generated           : AT91 SW Application Group  05/20/2005 (16:22:23) */
/** */
/** CVS Reference       : /lib_dbgu.h/1.1/Fri Jan 31 12:18:40 2003// */
/** CVS Reference       : /lib_pmc_SAM7X.h/1.1/Tue Feb  1 08:32:10 2005// */
/** CVS Reference       : /lib_VREG_6085B.h/1.1/Tue Feb  1 16:20:47 2005// */
/** CVS Reference       : /lib_rstc_6098A.h/1.1/Wed Oct  6 10:39:20 2004// */
/** CVS Reference       : /lib_ssc.h/1.4/Fri Jan 31 12:19:20 2003// */
/** CVS Reference       : /lib_wdtc_6080A.h/1.1/Wed Oct  6 10:38:30 2004// */
/** CVS Reference       : /lib_usart.h/1.5/Thu Nov 21 16:01:54 2002// */
/** CVS Reference       : /lib_spi2.h/1.1/Mon Aug 25 14:23:52 2003// */
/** CVS Reference       : /lib_pitc_6079A.h/1.2/Tue Nov  9 14:43:56 2004// */
/** CVS Reference       : /lib_aic_6075b.h/1.1/Fri May 20 14:01:19 2005// */
/** CVS Reference       : /lib_aes_6149a.h/1.1/Mon Jan 17 07:43:09 2005// */
/** CVS Reference       : /lib_twi.h/1.3/Mon Jul 19 14:27:58 2004// */
/** CVS Reference       : /lib_adc.h/1.6/Fri Oct 17 09:12:38 2003// */
/** CVS Reference       : /lib_rttc_6081A.h/1.1/Wed Oct  6 10:39:38 2004// */
/** CVS Reference       : /lib_udp.h/1.4/Wed Feb 16 08:39:34 2005// */
/** CVS Reference       : /lib_des3_6150a.h/1.1/Mon Jan 17 09:19:19 2005// */
/** CVS Reference       : /lib_tc_1753b.h/1.1/Fri Jan 31 12:20:02 2003// */
/** CVS Reference       : /lib_MC_SAM7X.h/1.1/Thu Mar 25 15:19:14 2004// */
/** CVS Reference       : /lib_pio.h/1.3/Fri Jan 31 12:18:56 2003// */
/** CVS Reference       : /lib_can_AT91.h/1.4/Fri Oct 17 09:12:50 2003// */
/** CVS Reference       : /lib_PWM_SAM.h/1.3/Thu Jan 22 10:10:50 2004// */
/** CVS Reference       : /lib_pdc.h/1.2/Tue Jul  2 13:29:40 2002// */
/** ---------------------------------------------------------------------------- */
#ifndef lib_AT91SAM7X128_H
    #define lib_AT91SAM7X128_H

/* *****************************************************************************
*               SOFTWARE API FOR AIC
***************************************************************************** */
    #define AT91C_AIC_BRANCH_OPCODE    ( ( void ( * )() ) 0xE51FFF20 ) /* ldr, pc, [pc, #-&F20] */

/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_ConfigureIt */
/** \brief Interrupt Handler Initialization */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_AIC_ConfigureIt( AT91PS_AIC pAic,                /* \arg pointer to the AIC registers */
                                                 unsigned int irq_id,            /* \arg interrupt number to initialize */
                                                 unsigned int priority,          /* \arg priority to give to the interrupt */
                                                 unsigned int src_type,          /* \arg activation and sense of activation */
                                                 void ( * newHandler )( void ) ) /* \arg address of the interrupt handler */
    {
        unsigned int oldHandler;
        unsigned int mask;

        oldHandler = pAic->AIC_SVR[ irq_id ];

        mask = 0x1 << irq_id;
        /** Disable the interrupt on the interrupt controller */
        pAic->AIC_IDCR = mask;
        /** Save the interrupt handler routine pointer and the interrupt priority */
        pAic->AIC_SVR[ irq_id ] = ( unsigned int ) newHandler;
        /** Store the Source Mode Register */
        pAic->AIC_SMR[ irq_id ] = src_type | priority;
        /** Clear the interrupt on the interrupt controller */
        pAic->AIC_ICCR = mask;

        return oldHandler;
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 2: 代码片段 2

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_EnableIt */
/** \brief Enable corresponding IT number */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_AIC_EnableIt( AT91PS_AIC pAic,      /* \arg pointer to the AIC registers */
                                      unsigned int irq_id ) /* \arg interrupt number to initialize */
    {
        /** Enable the interrupt on the interrupt controller */
        pAic->AIC_IECR = 0x1 << irq_id;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 3

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_DisableIt */
/** \brief Disable corresponding IT number */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_AIC_DisableIt( AT91PS_AIC pAic,      /* \arg pointer to the AIC registers */
                                       unsigned int irq_id ) /* \arg interrupt number to initialize */
    {
        unsigned int mask = 0x1 << irq_id;

        /** Disable the interrupt on the interrupt controller */
        pAic->AIC_IDCR = mask;
        /** Clear the interrupt on the Interrupt Controller ( if one is pending ) */
        pAic->AIC_ICCR = mask;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_ClearIt */
/** \brief Clear corresponding IT number */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_AIC_ClearIt( AT91PS_AIC pAic,      /* \arg pointer to the AIC registers */
                                     unsigned int irq_id ) /* \arg interrupt number to initialize */
    {
        /** Clear the interrupt on the Interrupt Controller ( if one is pending ) */
        pAic->AIC_ICCR = ( 0x1 << irq_id );
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_AcknowledgeIt */
/** \brief Acknowledge corresponding IT number */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_AIC_AcknowledgeIt( AT91PS_AIC pAic ) /* \arg pointer to the AIC registers */
    {
        pAic->AIC_EOICR = pAic->AIC_EOICR;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 函数 AT91F_AIC_SetExceptionVector

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_SetExceptionVector */
/** \brief Configure vector handler */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_AIC_SetExceptionVector( unsigned int * pVector, /* \arg pointer to the AIC registers */
                                                        void ( * Handler )() )  /* \arg Interrupt Handler */
    {
        unsigned int oldVector = *pVector;

        if( ( unsigned int ) Handler == ( unsigned int ) AT91C_AIC_BRANCH_OPCODE )
        {
            *pVector = ( unsigned int ) AT91C_AIC_BRANCH_OPCODE;
        }
        else
        {
            *pVector = ( ( ( ( ( unsigned int ) Handler ) - ( ( unsigned int ) pVector ) - 0x8 ) >> 2 ) & 0x00FFFFFF ) | 0xEA000000;
        }

        return oldVector;
    }
```

**解说：** 这一段实现函数 `AT91F_AIC_SetExceptionVector`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 代码片段 7

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_Trig */
/** \brief Trig an IT */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_AIC_Trig( AT91PS_AIC pAic,      /* \arg pointer to the AIC registers */
                                  unsigned int irq_id ) /* \arg interrupt number */
    {
        pAic->AIC_ISCR = ( 0x1 << irq_id );
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_IsActive */
/** \brief Test if an IT is active */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_AIC_IsActive( AT91PS_AIC pAic,      /* \arg pointer to the AIC registers */
                                              unsigned int irq_id ) /* \arg Interrupt Number */
    {
        return( pAic->AIC_ISR & ( 0x1 << irq_id ) );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 9: 代码片段 9

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_IsPending */
/** \brief Test if an IT is pending */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_AIC_IsPending( AT91PS_AIC pAic,      /* \arg pointer to the AIC registers */
                                               unsigned int irq_id ) /* \arg Interrupt Number */
    {
        return( pAic->AIC_IPR & ( 0x1 << irq_id ) );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 10: 函数 AT91F_AIC_Open

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_AIC_Open */
/** \brief Set exception vectors and AIC registers to default values */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_AIC_Open( AT91PS_AIC pAic,              /* \arg pointer to the AIC registers */
                                  void ( * IrqHandler )(),      /* \arg Default IRQ vector exception */
                                  void ( * FiqHandler )(),      /* \arg Default FIQ vector exception */
                                  void ( * DefaultHandler )(),  /* \arg Default Handler set in ISR */
                                  void ( * SpuriousHandler )(), /* \arg Default Spurious Handler */
                                  unsigned int protectMode )    /* \arg Debug Control Register */
    {
        int i;

        /* Disable all interrupts and set IVR to the default handler */
        for( i = 0; i < 32; ++i )
        {
            AT91F_AIC_DisableIt( pAic, i );
            AT91F_AIC_ConfigureIt( pAic, i, AT91C_AIC_PRIOR_LOWEST, AT91C_AIC_SRCTYPE_HIGH_LEVEL, DefaultHandler );
        }

        /* Set the IRQ exception vector */
        AT91F_AIC_SetExceptionVector( ( unsigned int * ) 0x18, IrqHandler );
        /* Set the Fast Interrupt exception vector */
        AT91F_AIC_SetExceptionVector( ( unsigned int * ) 0x1C, FiqHandler );

        pAic->AIC_SPU = ( unsigned int ) SpuriousHandler;
        pAic->AIC_DCR = protectMode;
    }
```

**解说：** 这一段实现函数 `AT91F_AIC_Open`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 11: 代码片段 11

```c
/* *****************************************************************************
*               SOFTWARE API FOR PDC
***************************************************************************** */
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_SetNextRx */
/** \brief Set the next receive transfer descriptor */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_SetNextRx( AT91PS_PDC pPDC,     /* \arg pointer to a PDC controller */
                                       char * address,      /* \arg address to the next block to be received */
                                       unsigned int bytes ) /* \arg number of bytes to be received */
    {
        pPDC->PDC_RNPR = ( unsigned int ) address;
        pPDC->PDC_RNCR = bytes;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_SetNextTx */
/** \brief Set the next transmit transfer descriptor */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_SetNextTx( AT91PS_PDC pPDC,     /* \arg pointer to a PDC controller */
                                       char * address,      /* \arg address to the next block to be transmitted */
                                       unsigned int bytes ) /* \arg number of bytes to be transmitted */
    {
        pPDC->PDC_TNPR = ( unsigned int ) address;
        pPDC->PDC_TNCR = bytes;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 代码片段 13

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_SetRx */
/** \brief Set the receive transfer descriptor */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_SetRx( AT91PS_PDC pPDC,     /* \arg pointer to a PDC controller */
                                   char * address,      /* \arg address to the next block to be received */
                                   unsigned int bytes ) /* \arg number of bytes to be received */
    {
        pPDC->PDC_RPR = ( unsigned int ) address;
        pPDC->PDC_RCR = bytes;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 代码片段 14

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_SetTx */
/** \brief Set the transmit transfer descriptor */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_SetTx( AT91PS_PDC pPDC,     /* \arg pointer to a PDC controller */
                                   char * address,      /* \arg address to the next block to be transmitted */
                                   unsigned int bytes ) /* \arg number of bytes to be transmitted */
    {
        pPDC->PDC_TPR = ( unsigned int ) address;
        pPDC->PDC_TCR = bytes;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 代码片段 15

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_EnableTx */
/** \brief Enable transmit */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_EnableTx( AT91PS_PDC pPDC ) /* \arg pointer to a PDC controller */
    {
        pPDC->PDC_PTCR = AT91C_PDC_TXTEN;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 代码片段 16

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_EnableRx */
/** \brief Enable receive */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_EnableRx( AT91PS_PDC pPDC ) /* \arg pointer to a PDC controller */
    {
        pPDC->PDC_PTCR = AT91C_PDC_RXTEN;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 代码片段 17

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_DisableTx */
/** \brief Disable transmit */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_DisableTx( AT91PS_PDC pPDC ) /* \arg pointer to a PDC controller */
    {
        pPDC->PDC_PTCR = AT91C_PDC_TXTDIS;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 18: 代码片段 18

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_DisableRx */
/** \brief Disable receive */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_DisableRx( AT91PS_PDC pPDC ) /* \arg pointer to a PDC controller */
    {
        pPDC->PDC_PTCR = AT91C_PDC_RXTDIS;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 代码片段 19

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_IsTxEmpty */
/** \brief Test if the current transfer descriptor has been sent */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PDC_IsTxEmpty( /* \return return 1 if transfer is complete */
        AT91PS_PDC pPDC )             /* \arg pointer to a PDC controller */
    {
        return !( pPDC->PDC_TCR );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 20: 代码片段 20

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_IsNextTxEmpty */
/** \brief Test if the next transfer descriptor has been moved to the current td */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PDC_IsNextTxEmpty( /* \return return 1 if transfer is complete */
        AT91PS_PDC pPDC )                 /* \arg pointer to a PDC controller */
    {
        return !( pPDC->PDC_TNCR );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 21: 代码片段 21

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_IsRxEmpty */
/** \brief Test if the current transfer descriptor has been filled */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PDC_IsRxEmpty( /* \return return 1 if transfer is complete */
        AT91PS_PDC pPDC )             /* \arg pointer to a PDC controller */
    {
        return !( pPDC->PDC_RCR );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 22: 代码片段 22

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_IsNextRxEmpty */
/** \brief Test if the next transfer descriptor has been moved to the current td */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PDC_IsNextRxEmpty( /* \return return 1 if transfer is complete */
        AT91PS_PDC pPDC )                 /* \arg pointer to a PDC controller */
    {
        return !( pPDC->PDC_RNCR );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 23: 代码片段 23

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_Open */
/** \brief Open PDC: disable TX and RX reset transfer descriptors, re-enable RX and TX */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_Open( AT91PS_PDC pPDC ) /* \arg pointer to a PDC controller */
    {
        /** Disable the RX and TX PDC transfer requests */
        AT91F_PDC_DisableRx( pPDC );
        AT91F_PDC_DisableTx( pPDC );

        /** Reset all Counter register Next buffer first */
        AT91F_PDC_SetNextTx( pPDC, ( char * ) 0, 0 );
        AT91F_PDC_SetNextRx( pPDC, ( char * ) 0, 0 );
        AT91F_PDC_SetTx( pPDC, ( char * ) 0, 0 );
        AT91F_PDC_SetRx( pPDC, ( char * ) 0, 0 );

        /** Enable the RX and TX PDC transfer requests */
        AT91F_PDC_EnableRx( pPDC );
        AT91F_PDC_EnableTx( pPDC );
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 24: 代码片段 24

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_Close */
/** \brief Close PDC: disable TX and RX reset transfer descriptors */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PDC_Close( AT91PS_PDC pPDC ) /* \arg pointer to a PDC controller */
    {
        /** Disable the RX and TX PDC transfer requests */
        AT91F_PDC_DisableRx( pPDC );
        AT91F_PDC_DisableTx( pPDC );

        /** Reset all Counter register Next buffer first */
        AT91F_PDC_SetNextTx( pPDC, ( char * ) 0, 0 );
        AT91F_PDC_SetNextRx( pPDC, ( char * ) 0, 0 );
        AT91F_PDC_SetTx( pPDC, ( char * ) 0, 0 );
        AT91F_PDC_SetRx( pPDC, ( char * ) 0, 0 );
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 25: 函数 AT91F_PDC_SendFrame

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_SendFrame */
/** \brief Close PDC: disable TX and RX reset transfer descriptors */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PDC_SendFrame( AT91PS_PDC pPDC,
                                               char * pBuffer,
                                               unsigned int szBuffer,
                                               char * pNextBuffer,
                                               unsigned int szNextBuffer )
    {
        if( AT91F_PDC_IsTxEmpty( pPDC ) )
        {
            /** Buffer and next buffer can be initialized */
            AT91F_PDC_SetTx( pPDC, pBuffer, szBuffer );
            AT91F_PDC_SetNextTx( pPDC, pNextBuffer, szNextBuffer );
            return 2;
        }
        else if( AT91F_PDC_IsNextTxEmpty( pPDC ) )
        {
            /** Only one buffer can be initialized */
            AT91F_PDC_SetNextTx( pPDC, pBuffer, szBuffer );
            return 1;
        }
        else
        {
            /** All buffer are in use... */
            return 0;
        }
    }
```

**解说：** 这一段实现函数 `AT91F_PDC_SendFrame`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 26: 函数 AT91F_PDC_ReceiveFrame

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PDC_ReceiveFrame */
/** \brief Close PDC: disable TX and RX reset transfer descriptors */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PDC_ReceiveFrame( AT91PS_PDC pPDC,
                                                  char * pBuffer,
                                                  unsigned int szBuffer,
                                                  char * pNextBuffer,
                                                  unsigned int szNextBuffer )
    {
        if( AT91F_PDC_IsRxEmpty( pPDC ) )
        {
            /** Buffer and next buffer can be initialized */
            AT91F_PDC_SetRx( pPDC, pBuffer, szBuffer );
            AT91F_PDC_SetNextRx( pPDC, pNextBuffer, szNextBuffer );
            return 2;
        }
        else if( AT91F_PDC_IsNextRxEmpty( pPDC ) )
        {
            /** Only one buffer can be initialized */
            AT91F_PDC_SetNextRx( pPDC, pBuffer, szBuffer );
            return 1;
        }
        else
        {
            /** All buffer are in use... */
            return 0;
        }
    }
```

**解说：** 这一段实现函数 `AT91F_PDC_ReceiveFrame`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 27: 代码片段 27

```c
/* *****************************************************************************
*               SOFTWARE API FOR DBGU
***************************************************************************** */
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_DBGU_InterruptEnable */
/** \brief Enable DBGU Interrupt */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_DBGU_InterruptEnable( AT91PS_DBGU pDbgu,  /* \arg  pointer to a DBGU controller */
                                              unsigned int flag ) /* \arg  dbgu interrupt to be enabled */
    {
        pDbgu->DBGU_IER = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 28: 代码片段 28

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_DBGU_InterruptDisable */
/** \brief Disable DBGU Interrupt */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_DBGU_InterruptDisable( AT91PS_DBGU pDbgu,  /* \arg  pointer to a DBGU controller */
                                               unsigned int flag ) /* \arg  dbgu interrupt to be disabled */
    {
        pDbgu->DBGU_IDR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 代码片段 29

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_DBGU_GetInterruptMaskStatus */
/** \brief Return DBGU Interrupt Mask Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_DBGU_GetInterruptMaskStatus( /* \return DBGU Interrupt Mask Status */
        AT91PS_DBGU pDbgu )                                  /* \arg  pointer to a DBGU controller */
    {
        return pDbgu->DBGU_IMR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 30: 代码片段 30

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_DBGU_IsInterruptMasked */
/** \brief Test if DBGU Interrupt is Masked */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_DBGU_IsInterruptMasked( AT91PS_DBGU pDbgu,  /* \arg  pointer to a DBGU controller */
                                               unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_DBGU_GetInterruptMaskStatus( pDbgu ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 31: 代码片段 31

```c
/* *****************************************************************************
*               SOFTWARE API FOR PIO
***************************************************************************** */
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_CfgPeriph */
/** \brief Enable pins to be derived by peripheral */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_CfgPeriph( AT91PS_PIO pPio,             /* \arg pointer to a PIO controller */
                                       unsigned int periphAEnable,  /* \arg PERIPH A to enable */
                                       unsigned int periphBEnable ) /* \arg PERIPH B to enable */

    {
        pPio->PIO_ASR = periphAEnable;
        pPio->PIO_BSR = periphBEnable;
        pPio->PIO_PDR = ( periphAEnable | periphBEnable ); /* Set in Periph mode */
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 32: 代码片段 32

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_CfgOutput */
/** \brief Enable PIO in output mode */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_CfgOutput( AT91PS_PIO pPio,         /* \arg pointer to a PIO controller */
                                       unsigned int pioEnable ) /* \arg PIO to be enabled */
    {
        pPio->PIO_PER = pioEnable;                              /* Set in PIO mode */
        pPio->PIO_OER = pioEnable;                              /* Configure in Output */
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 33: 代码片段 33

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_CfgInput */
/** \brief Enable PIO in input mode */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_CfgInput( AT91PS_PIO pPio,           /* \arg pointer to a PIO controller */
                                      unsigned int inputEnable ) /* \arg PIO to be enabled */
    {
        /* Disable output */
        pPio->PIO_ODR = inputEnable;
        pPio->PIO_PER = inputEnable;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 34: 代码片段 34

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_CfgOpendrain */
/** \brief Configure PIO in open drain */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_CfgOpendrain( AT91PS_PIO pPio,              /* \arg pointer to a PIO controller */
                                          unsigned int multiDrvEnable ) /* \arg pio to be configured in open drain */
    {
        /* Configure the multi-drive option */
        pPio->PIO_MDDR = ~multiDrvEnable;
        pPio->PIO_MDER = multiDrvEnable;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 35: 代码片段 35

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_CfgPullup */
/** \brief Enable pullup on PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_CfgPullup( AT91PS_PIO pPio,            /* \arg pointer to a PIO controller */
                                       unsigned int pullupEnable ) /* \arg enable pullup on PIO */
    {
        /* Connect or not Pullup */
        pPio->PIO_PPUDR = ~pullupEnable;
        pPio->PIO_PPUER = pullupEnable;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 36: 代码片段 36

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_CfgDirectDrive */
/** \brief Enable direct drive on PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_CfgDirectDrive( AT91PS_PIO pPio,           /* \arg pointer to a PIO controller */
                                            unsigned int directDrive ) /* \arg PIO to be configured with direct drive */

    {
        /* Configure the Direct Drive */
        pPio->PIO_OWDR = ~directDrive;
        pPio->PIO_OWER = directDrive;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 37: 代码片段 37

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_CfgInputFilter */
/** \brief Enable input filter on input PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_CfgInputFilter( AT91PS_PIO pPio,           /* \arg pointer to a PIO controller */
                                            unsigned int inputFilter ) /* \arg PIO to be configured with input filter */

    {
        /* Configure the Direct Drive */
        pPio->PIO_IFDR = ~inputFilter;
        pPio->PIO_IFER = inputFilter;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 38: 代码片段 38

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetInput */
/** \brief Return PIO input value */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetInput( /* \return PIO input */
        AT91PS_PIO pPio )                     /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_PDSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 39: 代码片段 39

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsInputSet */
/** \brief Test if PIO is input flag is active */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsInputSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                       unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetInput( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 40: 代码片段 40

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_SetOutput */
/** \brief Set to 1 output PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_SetOutput( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                       unsigned int flag ) /* \arg  output to be set */
    {
        pPio->PIO_SODR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 41: 代码片段 41

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_ClearOutput */
/** \brief Set to 0 output PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_ClearOutput( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                         unsigned int flag ) /* \arg  output to be cleared */
    {
        pPio->PIO_CODR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 42: 代码片段 42

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_ForceOutput */
/** \brief Force output when Direct drive option is enabled */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_ForceOutput( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                         unsigned int flag ) /* \arg  output to be forced */
    {
        pPio->PIO_ODSR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 43: 代码片段 43

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_Enable */
/** \brief Enable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_Enable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                    unsigned int flag ) /* \arg  pio to be enabled */
    {
        pPio->PIO_PER = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 44: 代码片段 44

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_Disable */
/** \brief Disable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_Disable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                     unsigned int flag ) /* \arg  pio to be disabled */
    {
        pPio->PIO_PDR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 45: 代码片段 45

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetStatus */
/** \brief Return PIO Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetStatus( /* \return PIO Status */
        AT91PS_PIO pPio )                      /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_PSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 46: 代码片段 46

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsSet */
/** \brief Test if PIO is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                  unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 47: 代码片段 47

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_OutputEnable */
/** \brief Output Enable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_OutputEnable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                          unsigned int flag ) /* \arg  pio output to be enabled */
    {
        pPio->PIO_OER = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 48: 代码片段 48

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_OutputDisable */
/** \brief Output Enable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_OutputDisable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                           unsigned int flag ) /* \arg  pio output to be disabled */
    {
        pPio->PIO_ODR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 49: 代码片段 49

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetOutputStatus */
/** \brief Return PIO Output Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetOutputStatus( /* \return PIO Output Status */
        AT91PS_PIO pPio )                            /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_OSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 50: 代码片段 50

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsOuputSet */
/** \brief Test if PIO Output is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsOutputSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                        unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetOutputStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 51: 代码片段 51

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_InputFilterEnable */
/** \brief Input Filter Enable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_InputFilterEnable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                               unsigned int flag ) /* \arg  pio input filter to be enabled */
    {
        pPio->PIO_IFER = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 52: 代码片段 52

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_InputFilterDisable */
/** \brief Input Filter Disable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_InputFilterDisable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                                unsigned int flag ) /* \arg  pio input filter to be disabled */
    {
        pPio->PIO_IFDR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 53: 代码片段 53

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetInputFilterStatus */
/** \brief Return PIO Input Filter Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetInputFilterStatus( /* \return PIO Input Filter Status */
        AT91PS_PIO pPio )                                 /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_IFSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 54: 代码片段 54

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsInputFilterSet */
/** \brief Test if PIO Input filter is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsInputFilterSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                             unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetInputFilterStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 55: 代码片段 55

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetOutputDataStatus */
/** \brief Return PIO Output Data Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetOutputDataStatus( /* \return PIO Output Data Status */
        AT91PS_PIO pPio )                                /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_ODSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 56: 代码片段 56

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_InterruptEnable */
/** \brief Enable PIO Interrupt */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_InterruptEnable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                             unsigned int flag ) /* \arg  pio interrupt to be enabled */
    {
        pPio->PIO_IER = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 57: 代码片段 57

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_InterruptDisable */
/** \brief Disable PIO Interrupt */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_InterruptDisable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                              unsigned int flag ) /* \arg  pio interrupt to be disabled */
    {
        pPio->PIO_IDR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 58: 代码片段 58

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetInterruptMaskStatus */
/** \brief Return PIO Interrupt Mask Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetInterruptMaskStatus( /* \return PIO Interrupt Mask Status */
        AT91PS_PIO pPio )                                   /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_IMR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 59: 代码片段 59

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetInterruptStatus */
/** \brief Return PIO Interrupt Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetInterruptStatus( /* \return PIO Interrupt Status */
        AT91PS_PIO pPio )                               /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_ISR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 60: 代码片段 60

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsInterruptMasked */
/** \brief Test if PIO Interrupt is Masked */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsInterruptMasked( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                              unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetInterruptMaskStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 61: 代码片段 61

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsInterruptSet */
/** \brief Test if PIO Interrupt is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsInterruptSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                           unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetInterruptStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 62: 代码片段 62

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_MultiDriverEnable */
/** \brief Multi Driver Enable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_MultiDriverEnable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                               unsigned int flag ) /* \arg  pio to be enabled */
    {
        pPio->PIO_MDER = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 63: 代码片段 63

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_MultiDriverDisable */
/** \brief Multi Driver Disable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_MultiDriverDisable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                                unsigned int flag ) /* \arg  pio to be disabled */
    {
        pPio->PIO_MDDR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 64: 代码片段 64

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetMultiDriverStatus */
/** \brief Return PIO Multi Driver Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetMultiDriverStatus( /* \return PIO Multi Driver Status */
        AT91PS_PIO pPio )                                 /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_MDSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 65: 代码片段 65

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsMultiDriverSet */
/** \brief Test if PIO MultiDriver is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsMultiDriverSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                             unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetMultiDriverStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 66: 代码片段 66

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_A_RegisterSelection */
/** \brief PIO A Register Selection */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_A_RegisterSelection( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                                 unsigned int flag ) /* \arg  pio A register selection */
    {
        pPio->PIO_ASR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 67: 代码片段 67

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_B_RegisterSelection */
/** \brief PIO B Register Selection */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_B_RegisterSelection( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                                 unsigned int flag ) /* \arg  pio B register selection */
    {
        pPio->PIO_BSR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 68: 代码片段 68

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_Get_AB_RegisterStatus */
/** \brief Return PIO Interrupt Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_Get_AB_RegisterStatus( /* \return PIO AB Register Status */
        AT91PS_PIO pPio )                                  /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_ABSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 69: 代码片段 69

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsAB_RegisterSet */
/** \brief Test if PIO AB Register is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsAB_RegisterSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                             unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_Get_AB_RegisterStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 70: 代码片段 70

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_OutputWriteEnable */
/** \brief Output Write Enable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_OutputWriteEnable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                               unsigned int flag ) /* \arg  pio output write to be enabled */
    {
        pPio->PIO_OWER = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 71: 代码片段 71

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_OutputWriteDisable */
/** \brief Output Write Disable PIO */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PIO_OutputWriteDisable( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                                unsigned int flag ) /* \arg  pio output write to be disabled */
    {
        pPio->PIO_OWDR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 72: 代码片段 72

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetOutputWriteStatus */
/** \brief Return PIO Output Write Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetOutputWriteStatus( /* \return PIO Output Write Status */
        AT91PS_PIO pPio )                                 /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_OWSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 73: 代码片段 73

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsOutputWriteSet */
/** \brief Test if PIO OutputWrite is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsOutputWriteSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                             unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetOutputWriteStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 74: 代码片段 74

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_GetCfgPullup */
/** \brief Return PIO Configuration Pullup */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PIO_GetCfgPullup( /* \return PIO Configuration Pullup */
        AT91PS_PIO pPio )                         /* \arg  pointer to a PIO controller */
    {
        return pPio->PIO_PPUSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 75: 代码片段 75

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsOutputDataStatusSet */
/** \brief Test if PIO Output Data Status is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsOutputDataStatusSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                                  unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PIO_GetOutputDataStatus( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 76: 代码片段 76

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PIO_IsCfgPullupStatusSet */
/** \brief Test if PIO Configuration Pullup Status is Set */
/**---------------------------------------------------------------------------- */
    __inline int AT91F_PIO_IsCfgPullupStatusSet( AT91PS_PIO pPio,    /* \arg  pointer to a PIO controller */
                                                 unsigned int flag ) /* \arg  flag to be tested */
    {
        return( ~AT91F_PIO_GetCfgPullup( pPio ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 77: 函数 AT91F_PMC_CfgSysClkEnableReg

```c
/* *****************************************************************************
*               SOFTWARE API FOR PMC
***************************************************************************** */
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_CfgSysClkEnableReg */
/** \brief Configure the System Clock Enable Register of the PMC controller */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_CfgSysClkEnableReg( AT91PS_PMC pPMC, /* \arg pointer to PMC controller */
                                                unsigned int mode )
    {
        /** Write to the SCER register */
        pPMC->PMC_SCER = mode;
    }
```

**解说：** 这一段实现函数 `AT91F_PMC_CfgSysClkEnableReg`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 78: 函数 AT91F_PMC_CfgSysClkDisableReg

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_CfgSysClkDisableReg */
/** \brief Configure the System Clock Disable Register of the PMC controller */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_CfgSysClkDisableReg( AT91PS_PMC pPMC, /* \arg pointer to PMC controller */
                                                 unsigned int mode )
    {
        /** Write to the SCDR register */
        pPMC->PMC_SCDR = mode;
    }
```

**解说：** 这一段实现函数 `AT91F_PMC_CfgSysClkDisableReg`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 79: 函数 AT91F_PMC_GetSysClkStatusReg

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_GetSysClkStatusReg */
/** \brief Return the System Clock Status Register of the PMC controller */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PMC_GetSysClkStatusReg( AT91PS_PMC pPMC /* pointer to a CAN controller */
                                                        )
    {
        return pPMC->PMC_SCSR;
    }
```

**解说：** 这一段实现函数 `AT91F_PMC_GetSysClkStatusReg`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 80: 代码片段 80

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_EnablePeriphClock */
/** \brief Enable peripheral clock */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_EnablePeriphClock( AT91PS_PMC pPMC,         /* \arg pointer to PMC controller */
                                               unsigned int periphIds ) /* \arg IDs of peripherals to enable */
    {
        pPMC->PMC_PCER = periphIds;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 81: 代码片段 81

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_DisablePeriphClock */
/** \brief Disable peripheral clock */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_DisablePeriphClock( AT91PS_PMC pPMC,         /* \arg pointer to PMC controller */
                                                unsigned int periphIds ) /* \arg IDs of peripherals to enable */
    {
        pPMC->PMC_PCDR = periphIds;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 82: 代码片段 82

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_GetPeriphClock */
/** \brief Get peripheral clock status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PMC_GetPeriphClock( AT91PS_PMC pPMC ) /* \arg pointer to PMC controller */
    {
        return pPMC->PMC_PCSR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 83: 函数 AT91F_CKGR_CfgMainOscillatorReg

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_CKGR_CfgMainOscillatorReg */
/** \brief Cfg the main oscillator */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_CKGR_CfgMainOscillatorReg( AT91PS_CKGR pCKGR, /* \arg pointer to CKGR controller */
                                                   unsigned int mode )
    {
        pCKGR->CKGR_MOR = mode;
    }
```

**解说：** 这一段实现函数 `AT91F_CKGR_CfgMainOscillatorReg`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 84: 代码片段 84

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_CKGR_GetMainOscillatorReg */
/** \brief Cfg the main oscillator */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_CKGR_GetMainOscillatorReg( AT91PS_CKGR pCKGR ) /* \arg pointer to CKGR controller */
    {
        return pCKGR->CKGR_MOR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 85: 代码片段 85

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_CKGR_EnableMainOscillator */
/** \brief Enable the main oscillator */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_CKGR_EnableMainOscillator( AT91PS_CKGR pCKGR ) /* \arg pointer to CKGR controller */
    {
        pCKGR->CKGR_MOR |= AT91C_CKGR_MOSCEN;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 86: 代码片段 86

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_CKGR_DisableMainOscillator */
/** \brief Disable the main oscillator */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_CKGR_DisableMainOscillator( AT91PS_CKGR pCKGR ) /* \arg pointer to CKGR controller */
    {
        pCKGR->CKGR_MOR &= ~AT91C_CKGR_MOSCEN;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 87: 代码片段 87

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_CKGR_CfgMainOscStartUpTime */
/** \brief Cfg MORE Register according to the main osc startup time */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_CKGR_CfgMainOscStartUpTime( AT91PS_CKGR pCKGR,         /* \arg pointer to CKGR controller */
                                                    unsigned int startup_time, /* \arg main osc startup time in microsecond (us) */
                                                    unsigned int slowClock )   /* \arg slowClock in Hz */
    {
        pCKGR->CKGR_MOR &= ~AT91C_CKGR_OSCOUNT;
        pCKGR->CKGR_MOR |= ( ( slowClock * startup_time ) / ( 8 * 1000000 ) ) << 8;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 88: 代码片段 88

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_CKGR_GetMainClockFreqReg */
/** \brief Cfg the main oscillator */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_CKGR_GetMainClockFreqReg( AT91PS_CKGR pCKGR ) /* \arg pointer to CKGR controller */
    {
        return pCKGR->CKGR_MCFR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 89: 代码片段 89

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_CKGR_GetMainClock */
/** \brief Return Main clock in Hz */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_CKGR_GetMainClock( AT91PS_CKGR pCKGR,       /* \arg pointer to CKGR controller */
                                                   unsigned int slowClock ) /* \arg slowClock in Hz */
    {
        return ( ( pCKGR->CKGR_MCFR & AT91C_CKGR_MAINF ) * slowClock ) >> 4;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 90: 函数 AT91F_PMC_CfgMCKReg

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_CfgMCKReg */
/** \brief Cfg Master Clock Register */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_CfgMCKReg( AT91PS_PMC pPMC, /* \arg pointer to PMC controller */
                                       unsigned int mode )
    {
        pPMC->PMC_MCKR = mode;
    }
```

**解说：** 这一段实现函数 `AT91F_PMC_CfgMCKReg`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 91: 代码片段 91

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_GetMCKReg */
/** \brief Return Master Clock Register */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PMC_GetMCKReg( AT91PS_PMC pPMC ) /* \arg pointer to PMC controller */
    {
        return pPMC->PMC_MCKR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 92: 函数 AT91F_PMC_GetMasterClock

```c
/**------------------------------------------------------------------------------ */
/** \fn    AT91F_PMC_GetMasterClock */
/** \brief Return master clock in Hz which corresponds to processor clock for ARM7 */
/**------------------------------------------------------------------------------ */
    __inline unsigned int AT91F_PMC_GetMasterClock( AT91PS_PMC pPMC,         /* \arg pointer to PMC controller */
                                                    AT91PS_CKGR pCKGR,       /* \arg pointer to CKGR controller */
                                                    unsigned int slowClock ) /* \arg slowClock in Hz */
    {
        unsigned int reg = pPMC->PMC_MCKR;
        unsigned int prescaler = ( 1 << ( ( reg & AT91C_PMC_PRES ) >> 2 ) );
        unsigned int pllDivider, pllMultiplier;

        switch( reg & AT91C_PMC_CSS )
        {
            case AT91C_PMC_CSS_SLOW_CLK: /* Slow clock selected */
                return slowClock / prescaler;

            case AT91C_PMC_CSS_MAIN_CLK: /* Main clock is selected */
                return AT91F_CKGR_GetMainClock( pCKGR, slowClock ) / prescaler;

            case AT91C_PMC_CSS_PLL_CLK: /* PLLB clock is selected */
                reg = pCKGR->CKGR_PLLR;
                pllDivider = ( reg & AT91C_CKGR_DIV );
                pllMultiplier = ( ( reg & AT91C_CKGR_MUL ) >> 16 ) + 1;
                return AT91F_CKGR_GetMainClock( pCKGR, slowClock ) / pllDivider * pllMultiplier / prescaler;
        }

        return 0;
    }
```

**解说：** 这一段实现函数 `AT91F_PMC_GetMasterClock`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 93: 函数 AT91F_PMC_EnablePCK

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_EnablePCK */
/** \brief Enable peripheral clock */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_EnablePCK( AT91PS_PMC pPMC,  /* \arg pointer to PMC controller */
                                       unsigned int pck, /* \arg Peripheral clock identifier 0 .. 7 */
                                       unsigned int mode )
    {
        pPMC->PMC_PCKR[ pck ] = mode;
        pPMC->PMC_SCER = ( 1 << pck ) << 8;
    }
```

**解说：** 这一段实现函数 `AT91F_PMC_EnablePCK`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 94: 代码片段 94

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_DisablePCK */
/** \brief Enable peripheral clock */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_DisablePCK( AT91PS_PMC pPMC,   /* \arg pointer to PMC controller */
                                        unsigned int pck ) /* \arg Peripheral clock identifier 0 .. 7 */
    {
        pPMC->PMC_SCDR = ( 1 << pck ) << 8;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 95: 代码片段 95

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_EnableIt */
/** \brief Enable PMC interrupt */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_EnableIt( AT91PS_PMC pPMC,    /* pointer to a PMC controller */
                                      unsigned int flag ) /* IT to be enabled */
    {
        /** Write to the IER register */
        pPMC->PMC_IER = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 96: 代码片段 96

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_DisableIt */
/** \brief Disable PMC interrupt */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_PMC_DisableIt( AT91PS_PMC pPMC,    /* pointer to a PMC controller */
                                       unsigned int flag ) /* IT to be disabled */
    {
        /** Write to the IDR register */
        pPMC->PMC_IDR = flag;
    }
```

**解说：** 这一段是 `lib_AT91SAM7X128.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 97: 代码片段 97

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_GetStatus */
/** \brief Return PMC Interrupt Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PMC_GetStatus( /* \return PMC Interrupt Status */
        AT91PS_PMC pPMC )                      /* pointer to a PMC controller */
    {
        return pPMC->PMC_SR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 98: 代码片段 98

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_GetInterruptMaskStatus */
/** \brief Return PMC Interrupt Mask Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PMC_GetInterruptMaskStatus( /* \return PMC Interrupt Mask Status */
        AT91PS_PMC pPMC )                                   /* pointer to a PMC controller */
    {
        return pPMC->PMC_IMR;
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 99: 代码片段 99

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_IsInterruptMasked */
/** \brief Test if PMC Interrupt is Masked */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PMC_IsInterruptMasked( AT91PS_PMC pPMC,    /* \arg  pointer to a PMC controller */
                                                       unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PMC_GetInterruptMaskStatus( pPMC ) & flag );
    }
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 100: 函数 AT91F_PMC_IsStatusSet

```c
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PMC_IsStatusSet */
/** \brief Test if PMC Status is Set */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_PMC_IsStatusSet( AT91PS_PMC pPMC,    /* \arg  pointer to a PMC controller */
                                                 unsigned int flag ) /* \arg  flag to be tested */
    {
        return( AT91F_PMC_GetStatus( pPMC ) & flag );
    } /* *****************************************************************************
      *              SOFTWARE API FOR RSTC
      ***************************************************************************** */
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_RSTSoftReset */
/** \brief Start Software Reset */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_RSTSoftReset( AT91PS_RSTC pRSTC,
                                      unsigned int reset )
    {
        pRSTC->RSTC_RCR = ( 0xA5000000 | reset );
    }

/**---------------------------------------------------------------------------- */
/** \fn    AT91F_RSTSetMode */
/** \brief Set Reset Mode */
/**---------------------------------------------------------------------------- */
    __inline void AT91F_RSTSetMode( AT91PS_RSTC pRSTC,
                                    unsigned int mode )
    {
        pRSTC->RSTC_RMR = ( 0xA5000000 | mode );
    }

/**---------------------------------------------------------------------------- */
/** \fn    AT91F_RSTGetMode */
/** \brief Get Reset Mode */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_RSTGetMode( AT91PS_RSTC pRSTC )
    {
        return( pRSTC->RSTC_RMR );
    }

/**---------------------------------------------------------------------------- */
/** \fn    AT91F_RSTGetStatus */
/** \brief Get Reset Status */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_RSTGetStatus( AT91PS_RSTC pRSTC )
    {
        return( pRSTC->RSTC_RSR );
    }

/**---------------------------------------------------------------------------- */
/** \fn    AT91F_RSTIsSoftRstActive */
/** \brief Return !=0 if software reset is still not completed */
/**---------------------------------------------------------------------------- */
    __inline unsigned int AT91F_RSTIsSoftRstActive( AT91PS_RSTC pRSTC )
    {
        return( ( pRSTC->RSTC_RSR ) & AT91C_RSTC_SRCMP );
    }

/* *****************************************************************************
*               SOFTWARE API FOR RTTC
***************************************************************************** */
/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_SetRTT_TimeBase() */
/** \brief  Set the RTT prescaler according to the TimeBase in ms */
/**-------------------------------------------------------------------------------------- */
    __inline unsigned int AT91F_RTTSetTimeBase( AT91PS_RTTC pRTTC,
                                                unsigned int ms )
    {
        if( ms > 2000 )
        {
            return 1; /* AT91C_TIME_OUT_OF_RANGE */
        }

        pRTTC->RTTC_RTMR &= ~0xFFFF;
        pRTTC->RTTC_RTMR |= ( ( ( ms << 15 ) / 1000 ) & 0xFFFF );
        return 0;
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTTSetPrescaler() */
/** \brief  Set the new prescaler value */
/**-------------------------------------------------------------------------------------- */
    __inline unsigned int AT91F_RTTSetPrescaler( AT91PS_RTTC pRTTC,
                                                 unsigned int rtpres )
    {
        pRTTC->RTTC_RTMR &= ~0xFFFF;
        pRTTC->RTTC_RTMR |= ( rtpres & 0xFFFF );
        return( pRTTC->RTTC_RTMR );
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTTRestart() */
/** \brief  Restart the RTT prescaler */
/**-------------------------------------------------------------------------------------- */
    __inline void AT91F_RTTRestart( AT91PS_RTTC pRTTC )
    {
        pRTTC->RTTC_RTMR |= AT91C_RTTC_RTTRST;
    }


/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTT_SetAlarmINT() */
/** \brief  Enable RTT Alarm Interrupt */
/**-------------------------------------------------------------------------------------- */
    __inline void AT91F_RTTSetAlarmINT( AT91PS_RTTC pRTTC )
    {
        pRTTC->RTTC_RTMR |= AT91C_RTTC_ALMIEN;
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTT_ClearAlarmINT() */
/** \brief  Disable RTT Alarm Interrupt */
/**-------------------------------------------------------------------------------------- */
    __inline void AT91F_RTTClearAlarmINT( AT91PS_RTTC pRTTC )
    {
        pRTTC->RTTC_RTMR &= ~AT91C_RTTC_ALMIEN;
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTT_SetRttIncINT() */
/** \brief  Enable RTT INC Interrupt */
/**-------------------------------------------------------------------------------------- */
    __inline void AT91F_RTTSetRttIncINT( AT91PS_RTTC pRTTC )
    {
        pRTTC->RTTC_RTMR |= AT91C_RTTC_RTTINCIEN;
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTT_ClearRttIncINT() */
/** \brief  Disable RTT INC Interrupt */
/**-------------------------------------------------------------------------------------- */
    __inline void AT91F_RTTClearRttIncINT( AT91PS_RTTC pRTTC )
    {
        pRTTC->RTTC_RTMR &= ~AT91C_RTTC_RTTINCIEN;
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTT_SetAlarmValue() */
/** \brief  Set RTT Alarm Value */
/**-------------------------------------------------------------------------------------- */
    __inline void AT91F_RTTSetAlarmValue( AT91PS_RTTC pRTTC,
                                          unsigned int alarm )
    {
        pRTTC->RTTC_RTAR = alarm;
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTT_GetAlarmValue() */
/** \brief  Get RTT Alarm Value */
/**-------------------------------------------------------------------------------------- */
    __inline unsigned int AT91F_RTTGetAlarmValue( AT91PS_RTTC pRTTC )
    {
        return( pRTTC->RTTC_RTAR );
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTTGetStatus() */
/** \brief  Read the RTT status */
/**-------------------------------------------------------------------------------------- */
    __inline unsigned int AT91F_RTTGetStatus( AT91PS_RTTC pRTTC )
    {
        return( pRTTC->RTTC_RTSR );
    }

/**-------------------------------------------------------------------------------------- */
/** \fn     AT91F_RTT_ReadValue() */
/** \brief  Read the RTT value */
/**-------------------------------------------------------------------------------------- */
    __inline unsigned int AT91F_RTTReadValue( AT91PS_RTTC pRTTC )
    {
        register volatile unsigned int val1, val2;

        do
        {
            val1 = pRTTC->RTTC_RTVR;
            val2 = pRTTC->RTTC_RTVR;
        }
        while( val1 != val2 );

        return( val1 );
    }

/* *****************************************************************************
*               SOFTWARE API FOR PITC
***************************************************************************** */
/**---------------------------------------------------------------------------- */
/** \fn    AT91F_PITInit */
/** \brief System timer init : period in */
```

**解说：** 这一段实现函数 `AT91F_PMC_IsStatusSet`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。
