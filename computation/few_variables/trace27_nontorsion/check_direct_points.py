"""Independent polynomial identities for the direct square-abscissa charts.

No source builder or field-arithmetic producer is imported.  All calculations
below take place in the ordinary polynomial ring Z[h0,h1,Y].  Completeness of
the adaptive multiplier is proved in the accompanying square-abscissa paper;
it uses only the fact that 2 is not a rational cube.
"""
from finite_algebra_check_core import check, plus, times, power, expander


def verify_direct_points(source):
    nodes = source['coefficient_dag']
    variables = {v['name']: v['index'] for v in source['variables']}
    relations = {r['name']: r for r in source['finite_monic_relations']}
    events = [e for e in source['events'] if e['operation'] == 'point']
    check(len(events) == 9, 'Wrong number of direct point charts')
    one = {(): 1}
    h0, h1, Y = ({(i,): 1} for i in range(3))
    A0 = plus(power(h0, 4), times({(): 12}, power(h0, 2), power(h1, 2)),
              times({(): 4}, power(h1, 4)), {(): -11})
    B0 = plus(times({(): 4}, power(h0, 3), h1),
              times({(): 8}, h0, power(h1, 3)), {(): 6})
    multiplier0 = plus(times({(): 2}, A0), B0)
    multiplier1 = plus(times({(): -1}, A0), times({(): -1}, B0))
    A = plus(times({(): 6}, power(A0, 3)),
             times({(): -9}, A0, power(B0, 2)), times({(): -4}, power(B0, 3)))
    B = plus(times({(): -4}, power(A0, 3)),
             times({(): 6}, A0, power(B0, 2)), times({(): 3}, power(B0, 3)))
    N = plus(times({(): 2}, power(A0, 2)), times({(): -1}, power(B0, 2)))
    j0_num = plus(times(multiplier0, power(Y, 2)),
                  times({(): -4}, multiplier1, B))
    j1_num = plus(times({(): 2}, multiplier0, B),
                  times({(): -1}, multiplier1, power(Y, 2)))
    common_den = times({(): 2}, Y, N)
    x0 = plus(power(h0, 2), times({(): 2}, power(h1, 2)))
    x1 = times({(): 2}, h0, h1)
    y0_num = plus(times(h0, j0_num), times({(): 2}, h1, j1_num))
    y1_num = plus(times(h0, j1_num), times(h1, j0_num))
    coefficient_expected = [times({(): 8}, power(B, 2)), {},
                            times({(): -4}, A), {}]
    derivative_expected = plus(times({(): 4}, power(Y, 3)),
                               times({(): -8}, A, Y))
    for event in events:
        name = event['name']
        relation = relations[name + '.Y']
        expand = expander(nodes, variables={variables[name + '.a0']: 0,
                                           variables[name + '.a1']: 1,
                                           relation['variable']: 2})

        def equal(row, num, den=one):
            check(times(expand(row['numerator']), den) ==
                  times(num, expand(row['denominator'])),
                  'Incorrect direct point identity at ' + name)

        check(event['chart'] == 'x=h^2; y=h*j; j^2=h^4-D',
              'Unexpected point chart')
        check([expand(i) for i in relation['coefficient_nodes_ascending']] ==
              coefficient_expected, 'Incorrect transformed point quartic')
        check(expand(relation['derivative_guard']) == derivative_expected,
              'Incorrect transformed quartic derivative')
        check(relation['derivative_guard'] in source['guard_numerators'] and
              relation['generator_node'] in source['guard_numerators'],
              'Missing point root or derivative guard')
        check([expand(k) for k in relation['automatic_nonzero_nodes']] == [
              Y, plus(power(A, 2), times({(): -2}, power(B, 2))),
              derivative_expected, N], 'Changed automatic chart factors')
        for row, val in zip(event['square_root_x'], (h0, h1)): equal(row, val)
        for row, val in zip(event['original_radicand'], (A0, B0)): equal(row, val)
        for row, val in zip(event['multiplier'], (multiplier0, multiplier1)): equal(row, val)
        for row, val in zip(event['transformed_radicand'], (A, B)): equal(row, val)
        equal(event['transformed_j'][0], Y, {(): 2})
        equal(event['transformed_j'][1], B, Y)
        equal(event['j'][0], j0_num, common_den)
        equal(event['j'][1], j1_num, common_den)
        equal(event['output_x'][0], x0)
        equal(event['output_x'][1], x1)
        equal(event['output_y'][0], y0_num, common_den)
        equal(event['output_y'][1], y1_num, common_den)
    return {'direct_square_abscissa_charts_checked': len(events),
            'automatic_point_guards_checked': 4*len(events),
            'direct_point_identities_checked_over': 'Z[h0,h1,Y]',
            'adaptive_multiplier': '(2*A+B)-(A+B)*sqrt(2), where j^2=A+B*sqrt(2)',
            'point_chart_extra_finite_cases': 1,
            'point_chart_extra_retained_variables': 0,
            'nonvanishing_proof': 'The rational component equals 2*(u^3-2*v^3);2 is not a rational cube.'}
