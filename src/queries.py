class Queries():
    def __init__(self):
        pass

    def busca_rt_sap(self):
        query = """select * from (select rcte.DocEntry, rcte.U_Status, rcte.U_CodOperaca, rctt.U_CodTalhao, unpt.DocEntry ID_talhao, rcte.U_Data, rctt.LineId
                                    ,row_number() over(partition by rcte.Docentry order by rctt.LineId asc) rw
                                    from [@agri_rcte] rcte
                                    left join [@agri_rctt] rctt on rctt.docentry = rcte.docentry
                                    left join [@agri_unpt] unpt on unpt.Code = rctt.U_CodTalhao
                                    where rcte.u_status != 'C' and rcte.u_data >= DATEADD(day, -180,cast(GETDATE() as date))) as rt where rw = 1"""
        return query

    def busca_dados_frota_sqlite(self):
        query = """
                select cdequipamento, 
                        dthr_registro, 
                        dthriniciooperac, 
                        dthroperacao, 
                        vltemposec, 
                        json_extract(return_json_monit_eqpm, '$.descEquipamento') as descEquipamento, 
                        json_extract(return_json_monit_eqpm, '$.descTalhao') as desctalhao, 
                        json_extract(return_json_monit_eqpm, '$.vlVelocidade') as vlvelocidade, 
                        json_extract(return_json_monit_eqpm, '$.cdOrdemServico') as cdordemservico, 
                        json_extract(return_json_monit_eqpm, '$.cdOperacao') as cdoperacao, 
                        json_extract(return_json_monit_eqpm, '$.cdImplemento') as cdImplemento,
                        json_extract(return_json_monit_eqpm, '$.cdOperador') as cdOperador,
                        json_extract(return_json_monit_eqpm, '$.fgMonitoramentoAtivo') as fgmonitoramentoativo,
                        json_extract(return_json_monit_eqpm, '$.descEstado') as descestado, 
                        json_extract(return_json_monit_eqpm, '$.cdTalhao') as cdtalhao,
                        json_extract(return_json_monit_eqpm, '$.descFazenda') as descfazenda,
                        json_extract(return_json_monit_eqpm, '$.dtHrLocal') as datahora
                        ,return_json_monit_eqpm, return_json_eqpm_popup
                    from frotas_sap
                    order by cdequipamento asc;"""
        return query

    def ultima_comunicacao(self):
        query = """SELECT 
                    cdEquipamento, json_extract(return_json_monit_eqpm, '$.descEquipamento') as descricao, 
                    json_extract(return_json_monit_eqpm, '$.dtHrLocal') as datahora
                FROM frotas_sap"""
        return query